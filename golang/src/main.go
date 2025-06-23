package main

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type UserData struct {
	Name      string `json:"name"`
	Email     string `json:"email"`
	CreatedAt time.Time
}

func setupRouter() *gin.Engine {
	r := gin.Default()

	r.GET("/ping", func(c *gin.Context) {
		c.String(http.StatusOK, "pong")
	})

	r.POST("/user", func(c *gin.Context) {
		var user UserData
		if err := c.BindJSON(&user); err != nil {
			return
		}

		user.CreatedAt = time.Now()
		c.IndentedJSON(http.StatusCreated, user)
	})

	return r
}

func main() {
	r := setupRouter()
	r.Run(":8080")
}
