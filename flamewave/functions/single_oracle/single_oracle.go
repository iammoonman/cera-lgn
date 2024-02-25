package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-lambda-go/lambda"
	tabletopsimulator "github.com/iammoonman/go-tabletop-simulator"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type MyEvent struct {
	OracleID string `json:"oracle_id"`
}

func HandleRequest(ctx context.Context, event *MyEvent) (*string, error) {
	if event == nil {
		return nil, fmt.Errorf("received nil event")
	}
	if len(event.OracleID) == 0 {
		return nil, nil
	}
	mongourl := os.Getenv("mongo")
	mongoclient, err := mongo.Connect(ctx, options.Client().ApplyURI(mongourl))
	if err != nil {
		log.Fatal(err)
	}
	coll := mongoclient.Database("flamewave").Collection("cards")
	x := coll.FindOne(ctx, bson.E{Key: "oracle_id", Value: event.OracleID})
	var l FlamewaveTTSCard
	x.Decode(l)
	var deck = tabletopsimulator.NewDeckObject()
	deck.ContainedObjects = append(deck.ContainedObjects, l.ContainedObjectsEntry)
	deck.CustomDeck[fmt.Sprintf("%d", 1)] = l.CustomDeckEntry
	deck.DeckIDs = append(deck.DeckIDs, 1)
	return &deck, nil
}

func main() {
	lambda.Start(HandleRequest)
}
