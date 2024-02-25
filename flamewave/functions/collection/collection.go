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
	Identifiers []FlamewaveIdentifier `json:"identifiers"`
}

func HandleRequest(ctx context.Context, event *MyEvent) (*string, error) {
	if event == nil {
		return nil, fmt.Errorf("received nil event")
	}
	mongourl := os.Getenv("mongo")
	mongoclient, err := mongo.Connect(ctx, options.Client().ApplyURI(mongourl))
	if err != nil {
		log.Fatal(err)
	}
	// var stuff []Identifier
	// stuff = append(stuff, Identifier{ScryfallId: "4d3f41dc-72f6-4346-b95f-4813addb5af0"})
	// stuff = append(stuff, Identifier{CollectorNumber: "1", SetCode: "lea", Quantity: 4})
	// stuff = append(stuff, Identifier{OracleId: "ca00eb17-e5c3-42c8-a665-431f5f95b67f"})
	var ASS = fmt.Sprintf("Bad list.")
	if len(event.Identifiers) == 0 || len(event.Identifiers) > 1000 {
		return &ASS, nil
	}
	coll := mongoclient.Database("flamewave").Collection("cards")
	var l []FlamewaveTTSCard
	// If flamewave_id in the list of flamewave ids from the identifiers
	// If scryfall_id in the list of scryfall ids...
	// etc
	lstRequests := make(bson.D, len(event.Identifiers))
	for i, thing := range event.Identifiers {
		if thing.FlamewaveId != "" {
			lstRequests[i] = bson.E{Key: "$and", Value: bson.D{
				{Key: "flamewave_id", Value: thing.FlamewaveId},
			}}
		} else if thing.ScryfallId != "" {
			lstRequests[i] = bson.E{Key: "$and", Value: bson.D{
				{Key: "scryfall_id", Value: thing.ScryfallId},
			}}
		} else if thing.CollectorNumber != "" && thing.SetCode != "" {
			lstRequests[i] = bson.E{Key: "$and", Value: bson.D{
				{Key: "cn", Value: thing.CollectorNumber},
				{Key: "set", Value: thing.SetCode},
			}}
		} else if thing.OracleId != "" {
			lstRequests[i] = bson.E{Key: "$and", Value: bson.D{
				{Key: "oracle_id", Value: thing.OracleId},
			}}
		} else {
			return &ASS, nil
		}
	}
	filter := bson.D{{Key: "$or", Value: lstRequests}}
	x, err := coll.Find(ctx, filter)
	if err != nil {
		log.Fatal(err)
	}
	x.All(context.TODO(), l)
	outputMap := make(map[string]IntermediateCardStruct)
	var deck = tabletopsimulator.NewDeckObject()
	for _, c := range l {
		for x, identity := range event.Identifiers {
			if len(identity.OracleId) > 0 && identity.OracleId == c.OracleID {
				if o, err := outputMap[c.OracleID]; !err {
					if !o.Priority {
						outputMap[c.OracleID] = IntermediateCardStruct{Card: &c, Priority: false}
					}
				}
			}
			if (identity.CollectorNumber == c.CollectorNumber && identity.SetCode == c.SetCode) || identity.ScryfallId == c.ScryfallID {
				outputMap[c.OracleID] = IntermediateCardStruct{Card: &c, Priority: true}
				event.Identifiers[x].OracleId = c.OracleID
			}
		}
	}
	for n, i := range event.Identifiers {
		for q := 0; q <= int(i.Quantity); q++ {
			var c = outputMap[i.OracleId]
			deck.ContainedObjects = append(deck.ContainedObjects, c.Card.ContainedObjectsEntry)
			deck.DeckIDs = append(deck.DeckIDs, int(n*100))
			deck.CustomDeck[fmt.Sprintf("%d", n)] = c.Card.CustomDeckEntry
		}
	}
	// outputSave := TTSSave{ObjectStates: []TTSDeckObject{deck}}
	// c.JSON(http.StatusOK, deck)
	return &deck, nil
}

func main() {
	lambda.Start(HandleRequest)
}

type IntermediateCardStruct struct {
	Card     *FlamewaveTTSCard
	Priority bool
}
