package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"os"
	"strings"

	scryfall "github.com/BlueMonday/go-scryfall"
	"github.com/gin-gonic/gin"
)

const RotatedViewAngleScript = "function onLoad()self.alt_view_angle=Vector(180,0,90)end"
const FlippedViewAngleScript = "function onLoad()self.alt_view_angle=Vector(180,0,180)end"

type Objects struct {
	ObjectStates []TTSCard `json:"ObjectStates"`
}

type Transform struct {
	ScaleX float32 `json:"scaleX"`
	ScaleY float32 `json:"scaleY"`
	ScaleZ float32 `json:"scaleZ"`
}

type Card struct {
	FaceURL      string `json:"FaceURL"`
	BackURL      string `json:"BackURL"`
	NumWidth     int    `json:"NumWidth"`
	NumHeight    int    `json:"NumHeight"`
	BackIsHidden bool   `json:"BackIsHidden"`
}

type TTSCard struct {
	Name        string             `json:"Name"`
	Transform   Transform          `json:"Transform"`
	CardID      int                `json:"CardID"`
	Nickname    string             `json:"Nickname"`
	Description string             `json:"Description"`
	Memo        string             `json:"Memo"`
	LuaScript   string             `json:"LuaScript,omitempty"`
	CustomDeck  map[string]Card    `json:"CustomDeck"`
	States      map[string]TTSCard `json:"States"`
}

type TTSDeck struct {
	Name             string    `json:"Name"`
	Transform        Transform `json:"Transform"`
	DeckIDs          []int     `json:"DeckIDs"`
	ContainedObjects []TTSCard `json:"ContainedObjects"`
}

func OracleTexter(s string) string {
	s = strings.Replace(s, "(", "[i](", -1)
	s = strings.Replace(s, ")", ")[/i]", -1)
	return s
}
func RarityTexter(s string) string {
	switch s {
	case "common":
		return "[ffffff]⌈C⌋[-]"
	case "uncommon":
		return "[6c848c]⌈U⌋[-]"
	case "rare":
		return "[c5b37c]⌈R⌋[-]"
	case "mythic":
		return "[f64800]⌈M⌋[-]"
	case "special":
		return "[905d98]⌈S⌋[-]"
	case "bonus":
		return "[9c202b]⌈B⌋[-]"
	default:
		return "[9c202b]⌈B⌋[-]"
	}
}

func NewDeck(TTSCards []TTSCard) TTSDeck {
	var w = TTSDeck{Name: "Deck", Transform: Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0}, DeckIDs: []int{}, ContainedObjects: TTSCards}
	for i := 0; i < len(TTSCards); i++ {
		w.DeckIDs = append(w.DeckIDs, TTSCards[i].CardID)
	}
	return w
}

func (d *TTSDeck) AddCard(TTSCard TTSCard) {
	d.ContainedObjects = append(d.ContainedObjects, TTSCard)
	d.DeckIDs = append(d.DeckIDs, TTSCard.CardID)
}

func (d *TTSDeck) AddCards(TTSCards []TTSCard) {
	d.ContainedObjects = append(d.ContainedObjects, TTSCards...)
	for i := 0; i < len(TTSCards); i++ {
		d.DeckIDs = append(d.DeckIDs, TTSCards[i].CardID)
	}
}

func NewCard(c scryfall.Card, i int) TTSCard {
	var hundred = i * 100
	var s_one = fmt.Sprintf("%d", i)
	var ttscard = TTSCard{
		Name:        "Card",
		Transform:   Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0},
		CardID:      hundred,
		Nickname:    "A Magic Card",
		Description: "Something went wrong with the parsing of the card data in this request, so now you're stuck with this description. Sorry about that. Contact Moon.",
		Memo:        "d3e7bc24-c2b0-4be3-b9d9-8a8d23b93bc7",
		LuaScript:   "",
		CustomDeck: map[string]Card{
			s_one: {FaceURL: "https://cards.scryfall.io/normal/front/8/6/8625b50d-474d-46dd-af84-0b267ed5fab3.jpg?1616041637", BackURL: "https://i.imgur.com/TyC0LWj.jpg", NumWidth: 1, NumHeight: 1, BackIsHidden: true},
		},
		States: map[string]TTSCard{},
	}
	if len(c.OracleID) == 0 {
		ttscard.Memo = *c.CardFaces[0].OracleID
	} else {
		ttscard.Memo = c.OracleID
	}
	if c.Layout == scryfall.LayoutNormal || c.Layout == scryfall.LayoutLeveler || c.Layout == scryfall.LayoutMeld || c.Layout == scryfall.LayoutSaga || c.Layout == scryfall.LayoutToken || c.Layout == scryfall.LayoutHost || c.Layout == scryfall.LayoutAugment || c.Layout == scryfall.LayoutEmblem || c.Layout == scryfall.LayoutPrototype || c.Layout == scryfall.LayoutMutate || c.Layout == scryfall.LayoutCase || c.Layout == scryfall.LayoutClass {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleTexter(c.OracleText)))
		if c.Power != nil {
			descriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.Power, *c.Toughness))
		}
		if c.Loyalty != nil {
			descriptionbuffer.WriteString(fmt.Sprintf("\nLoyalty: %s", *c.Loyalty))
		}
		ttscard.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ttscard.Nickname = namebuffer.String()
		if entry, ok := ttscard.CustomDeck[s_one]; ok {
			entry.FaceURL = c.ImageURIs.Normal
			ttscard.CustomDeck[s_one] = entry
		}
	}
	if c.Layout == scryfall.LayoutSplit {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[0].OracleText)))
		descriptionbuffer.WriteString(fmt.Sprintf("\n[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[1].OracleText)))
		ttscard.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ttscard.LuaScript = RotatedViewAngleScript
		ttscard.Nickname = namebuffer.String()
		if entry, ok := ttscard.CustomDeck[s_one]; ok {
			entry.FaceURL = c.ImageURIs.Normal
			ttscard.CustomDeck[s_one] = entry
		}
	}
	if c.Layout == scryfall.LayoutFlip {
		var frontdescriptionbuffer bytes.Buffer
		frontdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[0].OracleText)))
		if c.CardFaces[0].Power != nil && c.CardFaces[0].Toughness != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.CardFaces[0].Power, *c.CardFaces[0].Toughness))
		}
		var backdescriptionbuffer bytes.Buffer
		backdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[1].OracleText)))
		if c.CardFaces[1].Power != nil && c.CardFaces[1].Toughness != nil {
			backdescriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.CardFaces[1].Power, *c.CardFaces[1].Toughness))
		}
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %fMV", c.Name, c.TypeLine, c.CMC))
		ttscard.Nickname = namebuffer.String()
		if strings.Contains(c.CardFaces[0].TypeLine, "Battle") {
			ttscard.LuaScript = RotatedViewAngleScript
		}
		if entry, ok := ttscard.CustomDeck[s_one]; ok {
			entry.FaceURL = c.ImageURIs.Normal
			ttscard.CustomDeck[s_one] = entry
		}
		ttscard.Description = fmt.Sprintf("%s\n[6E6E6E]%s[-]", frontdescriptionbuffer.String(), backdescriptionbuffer.String())
		// The States indices are mutually exclusive to the outer deck. It's safe to use 100.
		ttscard.States["2"] = TTSCard{
			Name:        "Card",
			Transform:   Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0},
			CardID:      100,
			Nickname:    namebuffer.String(),
			Description: fmt.Sprintf("[6E6E6E]%s[-]\n%s", frontdescriptionbuffer.String(), backdescriptionbuffer.String()),
			Memo:        c.OracleID,
			LuaScript:   FlippedViewAngleScript,
			CustomDeck: map[string]Card{
				"100": {
					FaceURL:      c.ImageURIs.Normal,
					BackURL:      "https://i.imgur.com/TyC0LWj.jpg",
					NumWidth:     1,
					NumHeight:    1,
					BackIsHidden: true,
				},
			},
		}
	}
	if c.Layout == scryfall.LayoutTransform || c.Layout == scryfall.LayoutDoubleFacedToken || c.Layout == scryfall.LayoutModalDFC || c.Layout == scryfall.LayoutReversible || c.Layout == scryfall.LayoutArtSeries {
		var frontdescriptionbuffer bytes.Buffer
		frontdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[0].OracleText)))
		if c.CardFaces[0].Power != nil && c.CardFaces[0].Toughness != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.CardFaces[0].Power, *c.CardFaces[0].Toughness))
		}
		if c.CardFaces[0].Loyalty != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\nLoyalty: %s", *c.CardFaces[0].Loyalty))
		}
		if c.CardFaces[0].Defense != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\nDefense: %s", *c.CardFaces[0].Defense))
		}
		var backdescriptionbuffer bytes.Buffer
		backdescriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[1].OracleText)))
		if c.CardFaces[1].Power != nil && c.CardFaces[1].Toughness != nil {
			backdescriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.CardFaces[1].Power, *c.CardFaces[1].Toughness))
		}
		if c.CardFaces[1].Loyalty != nil {
			backdescriptionbuffer.WriteString(fmt.Sprintf("\nLoyalty: %s", *c.CardFaces[1].Loyalty))
		}
		if c.CardFaces[0].Defense != nil {
			frontdescriptionbuffer.WriteString(fmt.Sprintf("\nDefense: %s", *c.CardFaces[0].Defense))
		}
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ttscard.Nickname = namebuffer.String()
		if strings.Contains(c.CardFaces[0].TypeLine, "Battle") {
			ttscard.LuaScript = RotatedViewAngleScript
		}
		if entry, ok := ttscard.CustomDeck[s_one]; ok {
			entry.FaceURL = c.CardFaces[0].ImageURIs.Normal
			ttscard.CustomDeck[s_one] = entry
		}
		ttscard.Description = fmt.Sprintf("%s\n[6E6E6E]%s[-]", frontdescriptionbuffer.String(), backdescriptionbuffer.String())
		// The States indices are mutually exclusive to the outer deck. It's safe to use 100.
		ttscard.States["2"] = TTSCard{
			Name:        "Card",
			Transform:   Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0},
			CardID:      100,
			Nickname:    namebuffer.String(),
			Description: fmt.Sprintf("[6E6E6E]%s[-]\n%s", frontdescriptionbuffer.String(), backdescriptionbuffer.String()),
			Memo:        c.OracleID,
			LuaScript:   "",
			CustomDeck: map[string]Card{
				"100": {
					FaceURL:      c.CardFaces[1].ImageURIs.Normal,
					BackURL:      "https://i.imgur.com/TyC0LWj.jpg",
					NumWidth:     1,
					NumHeight:    1,
					BackIsHidden: true,
				},
			},
		}
	}
	if c.Layout == scryfall.LayoutAdventure {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[0].Name, c.CardFaces[0].ManaCost, c.CardFaces[0].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[0].OracleText)))
		if c.Power != nil && c.Toughness != nil {
			descriptionbuffer.WriteString(fmt.Sprintf("\n%s/%s", *c.Power, *c.Toughness))
		}
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.CardFaces[1].Name, c.CardFaces[1].ManaCost, c.CardFaces[1].TypeLine, RarityTexter(c.Rarity), OracleTexter(*c.CardFaces[1].OracleText)))
		ttscard.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ttscard.Nickname = namebuffer.String()
		if entry, ok := ttscard.CustomDeck[s_one]; ok {
			entry.FaceURL = c.ImageURIs.Normal
			ttscard.CustomDeck[s_one] = entry
		}
	}
	if c.Layout == scryfall.LayoutBattle {
		// No cards exist with this layout.
	}
	if c.Layout == scryfall.LayoutPlanar {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleTexter(c.OracleText)))
		ttscard.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ttscard.Nickname = namebuffer.String()
		ttscard.LuaScript = RotatedViewAngleScript
		if entry, ok := ttscard.CustomDeck[s_one]; ok {
			entry.FaceURL = c.ImageURIs.Normal
			ttscard.CustomDeck[s_one] = entry
		}
	}
	if c.Layout == scryfall.LayoutScheme {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleTexter(c.OracleText)))
		ttscard.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ttscard.Nickname = namebuffer.String()
		if entry, ok := ttscard.CustomDeck[s_one]; ok {
			entry.FaceURL = c.ImageURIs.Normal
			ttscard.CustomDeck[s_one] = entry
		}
	}
	if c.Layout == scryfall.LayoutVanguard {
		var descriptionbuffer bytes.Buffer
		descriptionbuffer.WriteString(fmt.Sprintf("[b]%s %s[/b]\n%s %s\n%s", c.Name, c.ManaCost, c.TypeLine, RarityTexter(c.Rarity), OracleTexter(c.OracleText)))
		descriptionbuffer.WriteString(fmt.Sprintf("\nHand Modifier: %s\nLife Modifier: %s", *c.HandModifier, *c.LifeModifier))
		ttscard.Description = descriptionbuffer.String()
		var namebuffer bytes.Buffer
		namebuffer.WriteString(fmt.Sprintf("%s\n%s %dMV", c.Name, c.TypeLine, uint8(c.CMC)))
		ttscard.Nickname = namebuffer.String()
		if entry, ok := ttscard.CustomDeck[s_one]; ok {
			entry.FaceURL = c.ImageURIs.Normal
			ttscard.CustomDeck[s_one] = entry
		}
	}
	return ttscard
}

type Identifier struct {
	ScryfallId      string `json:"scryfall_id"`
	OracleId        string `json:"oracle_id"`
	CollectorNumber string `json:"cn"`
	SetCode         string `json:"set"`
}

type IntermediateCard struct {
	Card     scryfall.Card
	Priority bool
}

func getStuff(c *gin.Context) {
	var stuff []Identifier
	stuff = append(stuff, Identifier{ScryfallId: "4d3f41dc-72f6-4346-b95f-4813addb5af0"})
	stuff = append(stuff, Identifier{ScryfallId: "ee3b2aaa-f04e-4a2a-8d5f-b3cc54605b28"})
	stuff = append(stuff, Identifier{OracleId: "ca00eb17-e5c3-42c8-a665-431f5f95b67f"})
	// if err := c.BindJSON(&stuff); err != nil {
	// 	return
	// }
	f, err := os.Open("../default-cards.json")
	if err != nil {
		log.Fatal(err)
	}
	if len(stuff) == 0 {
		return
	}
	var output []scryfall.Card
	output, err = decodeStream(f, stuff)
	if err != nil {
		log.Fatal(err)
	}
	c.JSON(http.StatusOK, output)
}

func main() {
	// ctx := context.Background()
	// client, err := scryfall.NewClient()
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// sco := scryfall.SearchCardsOptions{}
	// result, err := client.SearchCards(ctx, "aberrantresearcher", sco)
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// for i := 0; i < len(result.Cards); i++ {
	// 	log.Printf("%s", NewCard(*&result.Cards[i], i).Description)
	// }
	router := gin.Default()
	router.GET("/", getStuff)
	// router.GET("/playground", getStuff) // There's also a JSON representation for stuff here.
	// router.GET("/simulator", getStuff)  // Returns full JSON string for spawning an object. Pass directly into spawnObjectData.
	router.POST("/simulator/cards", getStuff)
	router.Run("localhost:8080")
}

func decodeStream(reader io.Reader, identifiers []Identifier) ([]scryfall.Card, error) {
	dec := json.NewDecoder(reader)
	var output []scryfall.Card = make([]scryfall.Card, len(identifiers))
	var outputMap map[string]IntermediateCard = make(map[string]IntermediateCard)
	// var o = []scryfall.Card{}
	// fmt.Printf("%T: %v\n", t, t)
	for dec.More() {
		var m scryfall.Card
		err := dec.Decode(&m)
		if err != nil {
			return []scryfall.Card{}, err
		}
		for _, identity := range identifiers {
			if identity.OracleId == m.OracleID && len(identity.OracleId) > 0 {
				if _, err := outputMap[m.OracleID]; !err {
					outputMap[m.OracleID] = IntermediateCard{Card: m, Priority: false}
				}
			} else if (identity.CollectorNumber == m.CollectorNumber && identity.SetCode == m.Set) || identity.ScryfallId == m.ID {
				outputMap[m.OracleID] = IntermediateCard{Card: m, Priority: true}
			}
		}
		// o = append(o, m)
		// fmt.Printf("%v: %v\n", m.Name, m.OracleID)
	}
	var ctr int8 = 0
	for _, v := range outputMap {
		output[ctr] = v.Card
		fmt.Printf("%s %s\n", v.Card.Name, v.Card.OracleID)
		ctr++
	}
	// fmt.Printf("%T: %v\n", t, t)
	return output, nil
}
