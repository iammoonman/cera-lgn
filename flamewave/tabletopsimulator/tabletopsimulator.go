package tabletopsimulator

type Transform struct {
	ScaleX float32 `json:"scaleX"`
	ScaleY float32 `json:"scaleY"`
	ScaleZ float32 `json:"scaleZ"`
}

type Save struct {
	ObjectStates []DeckObject `json:"ObjectStates"`
}

type DeckObject struct {
	Name             string                `json:"Name"`
	Transform        Transform             `json:"Transform"`
	DeckIDs          []int                 `json:"DeckIDs"`
	ContainedObjects []CardEntry           `json:"ContainedObjects"`
	CustomDeck       map[string]ImageEntry `json:"CustomDeck"`
}

type ImageEntry struct {
	FaceURL      string `json:"FaceURL"`
	BackURL      string `json:"BackURL"`
	NumWidth     uint8  `json:"NumWidth"`
	NumHeight    uint8  `json:"NumHeight"`
	BackIsHidden bool   `json:"BackIsHidden"`
}

type StateEntry struct {
	CustomDeck  map[string]ImageEntry `json:"CustomDeck"`
	Name        string                `json:"Name"`
	Transform   Transform             `json:"Transform"`
	Nickname    string                `json:"Nickname"`
	Description string                `json:"Description"`
	Memo        string                `json:"Memo"`
	CardID      uint32                `json:"CardID"`
	LuaScript   string                `json:"LuaScript"`
}

type CardEntry struct {
	Name        string                `json:"Name"`
	Transform   Transform             `json:"Transform"`
	Nickname    string                `json:"Nickname"`
	Description string                `json:"Description"`
	Memo        string                `json:"Memo"`
	States      map[string]StateEntry `json:"States"`
	LuaScript   string                `json:"LuaScript"`
}

func NewDeckObject() DeckObject {
	var w = DeckObject{Name: "Deck", Transform: Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0}, DeckIDs: []int{}, ContainedObjects: []CardEntry{}, CustomDeck: make(map[string]ImageEntry)}
	return w
}

func NewCardEntry(nickname string, description string, memo string) CardEntry {
	var c = CardEntry{Name: "Card", Transform: Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0}, Nickname: nickname, Description: description, Memo: memo, States: map[string]StateEntry{}, LuaScript: ""}
	return c
}

func NewImageEntry(f string, b string) ImageEntry {
	var i = ImageEntry{FaceURL: f, BackURL: b, NumWidth: 1, NumHeight: 1, BackIsHidden: true}
	return i
}

func NewStateEntry(nickname string, description string, memo string, luaScript string, image ImageEntry) StateEntry {
	var s = StateEntry{Name: "Card", Transform: Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0}, Nickname: nickname, CustomDeck: map[string]ImageEntry{}, Description: description, Memo: memo, CardID: 100, LuaScript: luaScript}
	s.CustomDeck["1"] = image
	return s
}

func NewTransform() Transform {
	return Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0}
}

type MaximalTransform struct {
	ScaleX float32 `json:"scaleX"`
	ScaleY float32 `json:"scaleY"`
	ScaleZ float32 `json:"scaleZ"`
	RotX   float32 `json:"rotX"`
	RotY   float32 `json:"rotY"`
	RotZ   float32 `json:"rotZ"`
	PosX   float32 `json:"posX"`
	PosY   float32 `json:"posY"`
	PosZ   float32 `json:"posZ"`
}

type MaximalCustomDeck struct {
	FaceURL      string `json:"FaceURL"`
	BackURL      string `json:"BackURL"`
	NumWidth     int    `json:"NumWidth"`
	NumHeight    int    `json:"NumHeight"`
	BackIsHidden bool   `json:"BackIsHidden"`
	UniqueBack   bool   `json:"UniqueBack"`
}

type MaximalVector struct {
	X float32 `json:"x"`
	Y float32 `json:"y"`
	Z float32 `json:"z"`
}

type MaximalColor struct {
	R float32 `json:"R"`
	G float32 `json:"G"`
	B float32 `json:"B"`
}

type MaximalCard struct {
	Name                 string                       `json:"Name"`
	Transform            MaximalTransform             `json:"Transform"`
	CustomDeck           map[string]MaximalCustomDeck `json:"CustomDeck"`
	GUID                 string                       `json:"GUID"`
	Nickname             string                       `json:"Nickname"`
	Description          string                       `json:"Description"`
	GMNotes              string                       `json:"GMNotes"`
	AltLookAngle         MaximalVector                `json:"AltLookAngle"`
	ColorDiffuse         MaximalColor                 `json:"ColorDiffuse"`
	LayoutGroupSortIndex int                          `json:"LayoutGroupSortIndex"`
	Value                int                          `json:"Value"`
	Locked               bool                         `json:"Locked"`
	Grid                 bool                         `json:"Grid"`
	Snap                 bool                         `json:"Snap"`
	IgnoreFoW            bool                         `json:"IgnoreFoW"`
	MeasureMovement      bool                         `json:"MeasureMovement"`
	DragSelectable       bool                         `json:"DragSelectable"`
	Autoraise            bool                         `json:"Autoraise"`
	Sticky               bool                         `json:"Sticky"`
	Tooltip              bool                         `json:"Tooltip"`
	GridProjection       bool                         `json:"GridProjection"`
	HideWhenFaceDown     bool                         `json:"HideWhenFaceDown"`
	Hands                bool                         `json:"Hands"`
	CardID               int                          `json:"CardID"`
	SidewaysCard         bool                         `json:"SidewaysCard"`
	LuaScript            string                       `json:"LuaScript"`
	LuaScriptState       string                       `json:"LuaScriptState"`
	XmlUI                string                       `json:"XmlUI"`
}
