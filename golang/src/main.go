package main

import (
	"database/sql"
	"encoding/base64"
	"fmt"
	"log"
	"math"
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/kelseyhightower/envconfig"
	_ "github.com/lib/pq"
)

type Config struct {
	Database *DbConfig
}

type DbConfig struct {
	Port int    `envconfig:"DB_PORT" default:"5432"`
	Host string `envconfig:"DB_HOST" default:"localhost"`
	User string `envconfig:"DB_USER" default:"myuser"`
	Pass string `envconfig:"DB_PASS" default:"mypass"`
	Name string `envconfig:"DB_NAME" default:"lingue"`
}

type UserData struct {
	Name      string    `json:"name"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
}

func setupRouter(db *sql.DB) *gin.Engine {
	r := gin.Default()

	r.GET("/ping", func(c *gin.Context) {
		c.String(http.StatusOK, "pong")
	})

	r.GET("/encode", func(c *gin.Context) {
		text := []byte(c.Query("text"))
		c.String(
			http.StatusOK,
			base64.StdEncoding.EncodeToString(text),
		)
	})

	r.GET("/sqrt_sum", func(c *gin.Context) {
		var result float64
		size, _ := strconv.Atoi(c.Query("size"))

		for i := range size {
			result += math.Sqrt(float64(i))
		}

		c.String(http.StatusOK, "%f", result)
	})

	r.POST("/user", func(c *gin.Context) {
		var user UserData
		if err := c.BindJSON(&user); err != nil {
			return
		}

		user.CreatedAt = time.Now()
		c.IndentedJSON(http.StatusCreated, user)
	})

	r.POST("/insert", func(c *gin.Context) {
		var user UserData
		if err := c.BindJSON(&user); err != nil {
			return
		}

		id := 0
		stmt := "INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id"
		err := db.QueryRow(stmt, user.Name, user.Email).Scan(&id)

		if err != nil {
			log.Println(err)
			c.String(http.StatusInternalServerError, "Insert error")
		}

		c.String(http.StatusCreated, string(id))
	})

	return r
}

func initDatabase() *sql.DB {
	var dbConf DbConfig
	err := envconfig.Process("", &dbConf)

	if err != nil {
		log.Panic(err)
	}

	psqlInfo := fmt.Sprintf(
		"host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		dbConf.Host, dbConf.Port, dbConf.User, dbConf.Pass, dbConf.Name,
	)

	log.Println(psqlInfo)

	db, err := sql.Open("postgres", psqlInfo)
	if err != nil {
		panic(err)
	}

	err = db.Ping()
	if err != nil {
		panic(err)
	}

	log.Println("Successfully connected to Postgres!")

	db.Query(`
		CREATE TABLE IF NOT EXISTS users (
			id		serial		PRIMARY KEY,
			name	char(128)   NOT NULL,
			email	char(128)   NOT NULL
		)
	`)

	log.Println("Users table has created.")
	return db
}

func main() {
	db := initDatabase()

	r := setupRouter(db)
	r.Run(":8080")

	defer db.Close()
}
