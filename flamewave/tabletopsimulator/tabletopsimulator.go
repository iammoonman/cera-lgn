package tabletopsimulator

type Transform struct {
	ScaleX float32 `json:"scaleX"`
	ScaleY float32 `json:"scaleY"`
	ScaleZ float32 `json:"scaleZ"`
}

type Save struct {
	ObjectStates []Deck `json:"ObjectStates"`
}

type Deck struct {
	Name             string               `json:"Name"`
	Transform        Transform            `json:"Transform"`
	DeckIDs          []int                `json:"DeckIDs"`
	ContainedObjects []Card               `json:"ContainedObjects"`
	CustomDeck       map[string]CardImage `json:"CustomDeck"`
}

type CardImage struct {
	FaceURL      string `json:"FaceURL"`
	BackURL      string `json:"BackURL"`
	NumWidth     uint8  `json:"NumWidth"`
	NumHeight    uint8  `json:"NumHeight"`
	BackIsHidden bool   `json:"BackIsHidden"`
}

type CardState struct {
	CustomDeck  map[string]CardImage `json:"CustomDeck"`
	Name        string               `json:"Name"`
	Transform   Transform            `json:"Transform"`
	Nickname    string               `json:"Nickname"`
	Description string               `json:"Description"`
	Memo        string               `json:"Memo"`
	CardID      uint32               `json:"CardID"`
	LuaScript   string               `json:"LuaScript"`
}

type Card struct {
	Name        string               `json:"Name"`
	Transform   Transform            `json:"Transform"`
	Nickname    string               `json:"Nickname"`
	Description string               `json:"Description"`
	Memo        string               `json:"Memo"`
	States      map[string]CardState `json:"States"`
	LuaScript   string               `json:"LuaScript"`
}

func NewDeckObject() Deck {
	var w = Deck{Name: "Deck", Transform: Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0}, DeckIDs: []int{}, ContainedObjects: []Card{}, CustomDeck: make(map[string]CardImage)}
	return w
}

func NewCardEntry(nickname string, description string, memo string) Card {
	var c = Card{Name: "Card", Transform: Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0}, Nickname: nickname, Description: description, Memo: memo, States: map[string]CardState{}, LuaScript: ""}
	return c
}

func NewImageEntry(f string, b string) CardImage {
	var i = CardImage{FaceURL: f, BackURL: b, NumWidth: 1, NumHeight: 1, BackIsHidden: true}
	return i
}

func NewStateEntry(nickname string, description string, memo string, luaScript string, image CardImage) CardState {
	var s = CardState{Name: "Card", Transform: Transform{ScaleX: 1.0, ScaleY: 1.0, ScaleZ: 1.0}, Nickname: nickname, CustomDeck: map[string]CardImage{}, Description: description, Memo: memo, CardID: 100, LuaScript: luaScript}
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

type MaximalTabState struct {
	Title        string
	Body         string
	Color        MaximalColor
	VisibleColor string
	Id           int
}

type MaximalGrid struct {
	Type         int           `json:"Type"`
	Lines        bool          `json:"Lines"`
	Color        MaximalColor  `json:"Color"`
	Opacity      float32       `json:"Opacity"`
	ThickLines   bool          `json:"ThickLines"`
	Snapping     bool          `json:"Snapping"`
	Offset       bool          `json:"Offset"`
	BothSnapping bool          `json:"BothSnapping"`
	XSize        float32       `json:"xSize"`
	YSize        float32       `json:"ySize"`
	PosOffset    MaximalVector `json:"PosOffset"`
}

type MaximalLighting struct {
	LightIntensity      float32
	LightColor          MaximalColor
	AmbientIntensity    float32
	AmbientType         int
	AmbientSkyColor     MaximalColor
	AmbientEquatorColor MaximalColor
	AmbientGroundColor  MaximalColor
	ReflectionIntensity float32
	LutIndex            int
	LutContribution     float32
}

type MaximalTurns struct {
	Enable              bool
	Type                int
	TurnOrder           []string
	Reverse             bool
	SkipEmpty           bool
	DisableInteractions bool
	PassTurns           bool
	TurnColor           string
}

type MaximalComponentTags struct {
	Labels []string
}

type MaximalSnapPoint struct {
	Position MaximalVector
}

type MaximalCamera struct {
	Position MaximalVector
	Rotation MaximalVector
	Distance float32
	Zoomed   bool
}

type MaximalHands struct {
	Enable        bool
	DisableUnused bool
	Hiding        int
}

type MaximalVectorLine struct {
	Points3   []MaximalVector
	Color     MaximalColor
	Thickness float32
	Rotation  MaximalVector
	Loop      bool
	Square    bool
}

type MaximalDecalState struct {
	Transform   MaximalTransform
	CustomDecal MaximalCustomDecal
}

type MaximalCustomDecal struct {
	Name     string
	ImageURL string
	Size     float32
}

type MaximalSave struct {
	SaveName       string
	EpochTime      int
	GameComplexity string
	Tags           []string
	GameMode       string
	Gravity        float32
	PlayArea       float32
	ComponentTags  MaximalComponentTags
	Date           string
	Table          string
	TableURL       string
	Sky            string
	SkyURL         string
	Note           string
	Rules          string
	XmlUI          string
	CustomUIAssets string
	LuaScript      string
	LuaScriptState string
	Grid           MaximalGrid
	LightingState  MaximalLighting
	HandsState     MaximalHands
	TurnsState     MaximalTurns
	VectorLines    []MaximalVectorLine
	ObjectStates   []MaximalObjectState
	SnapPoints     []MaximalSnapPoint
	DecalPallet    []MaximalCustomDecal
	Decals         []MaximalDecalState
	TabStates      map[string]MaximalTabState
	CameraStates   []MaximalCamera
	VersionNumber  string
}

type MaximalRotationValueState struct {
	Value    struct{}
	Rotation MaximalVector
}

type MaximalCustomImageState struct {
	ImageURL           string
	ImageSecondaryURL  string
	WidthScale         float32
	CustomDice         MaximalCustomDiceState
	CustomToken        MaximalCustomTokenState
	CustomJigsawPuzzle MaximalCustomJigsawPuzzleState
	CustomTile         MaximalCustomTileState
}

type MaximalCustomAssetbundleState struct {
	AssetbundleURL          string
	AssetbundleSecondaryURL string
	/* 0 = Plastic, 1 = Wood, 2 = Metal, 3 = Cardboard */
	MaterialIndex int
	/* 0 = Generic, 1 = Figurine, 2 = Dice, 3 = Coin, 4 = Board, 5 = Chip, 6 = Bag, 7 = Infinite */
	TypeIndex          int
	LoopingEffectIndex int
}

type MaximalCustomDiceState struct {
	Type MaximalDiceType
}

type MaximalDiceType struct{}

type MaximalCustomTokenState struct {
	Thickness           float32
	MergeDistancePixels float32
	Stackable           bool
}

type MaximalCustomTileState struct {
	/* 0 = Box, 1 = Hex, 2 = Circle, 3 = Rounded */
	Type      int
	Thickness float32
	Stackable bool
	Stretch   bool
}

type MaximalCustomJigsawPuzzleState struct {
	NumPuzzlePieces int
	ImageOnBoard    bool
}

type MaximalCustomMeshState struct {
	MeshURL       string
	DiffuseURL    string
	NormalURL     string
	ColliderURL   string
	Convex        bool
	MaterialIndex int
	TypeIndex     int
	CustomShader  MaximalCustomShaderState
	CastShadows   bool
}

type MaximalCustomShaderState struct {
	SpecularColor     MaximalColor
	SpecularIntensity float32
	SpecularSharpness float32
	FresnelStrength   float32
}

type MaximalFogOfWarSaveState struct {
	HideGmPointer     bool
	HideObjects       bool
	Height            float32
	RevealedLocations map[string]int
}

type MaximalFogOfWarRevealerSaveState struct {
	Active bool
	Range  float32
	Color  string
}
type MaximalClockSaveState struct {
	ClockState    string
	SecondsPassed int
	Paused        bool
}
type MaximalCounterState struct {
	Value int
}
type MaximalTabletState struct {
	PageURL string
}
type MaximalMp3PlayerState struct {
	SongTitle string
	Genre     string
	Volume    float32
	IsPlaying bool
	LoopOne   bool
	MenuTitle string
	Menu      string
}
type MaximalCalculatorState struct {
	Value  string
	Memory float32
}
type MaximalTextState struct {
	Text       string
	ColorState MaximalColor
	FontSize   int
}
type MaximalPhysicsMaterialState struct {
	StaticFriction  float32
	DynamicFriction float32
	Bounciness      float32
	FrictionCombine int
	BounceCombine   int
}
type MaximalRigidbodyState struct {
	Mass        float32
	Drag        float32
	AngularDrag float32
	UseGravity  bool
}
type MaximalJointFixedState struct {
	ConnectedBodyGUID string
	EnableCollision   bool
	Axis              MaximalVector
	Anchor            MaximalVector
	ConnectedAnchor   MaximalVector
	BreakForce        float32
	BreakTorgue       float32
}
type MaximalJointHingeState struct {
	ConnectedBodyGUID string
	EnableCollision   bool
	Axis              MaximalVector
	Anchor            MaximalVector
	ConnectedAnchor   MaximalVector
	BreakForce        float32
	BreakTorgue       float32
	UseLimits         bool
	// Limits            string
	UseMotor bool
	// Motor             string
	// Spring            string
}
type MaximalJointSpringState struct {
	ConnectedBodyGUID string
	EnableCollision   bool
	Axis              MaximalVector
	Anchor            MaximalVector
	ConnectedAnchor   MaximalVector
	BreakForce        float32
	BreakTorgue       float32
	Damper            float32
	MaxDistance       float32
	MinDistance       float32
	Spring            float32
}
type MaximalCustomAssetState struct {
	Name string
	URL  string
}

type MaximalObjectState struct {
	Name                string
	Transform           MaximalTransform
	Nickname            string
	Description         string
	ColorDiffuse        MaximalColor
	Locked              bool
	Grid                bool
	Snap                bool
	Autoraise           bool
	Sticky              bool
	Tooltip             bool
	GridProjection      bool
	HideWhenFaceDown    bool
	Hands               bool
	AltSound            bool
	MaterialIndex       int
	MeshIndex           int
	Layer               int
	Number              int
	CardID              int
	SidewaysCard        bool
	RPGmode             bool
	RPGdead             bool
	FogColor            string
	FogHidePointers     bool
	FogReverseHiding    bool
	FogSeethrough       bool
	DeckIDs             []int
	CustomDeck          map[string]MaximalCustomDeck
	CustomMesh          MaximalCustomMeshState
	CustomImage         MaximalCustomImageState
	CustomAssetbundle   MaximalCustomAssetbundleState
	FogOfWar            MaximalFogOfWarSaveState
	FogOfWarRevealer    MaximalFogOfWarRevealerSaveState
	Clock               MaximalClockSaveState
	Counter             MaximalCounterState
	Tablet              MaximalTabletState
	Mp3Player           MaximalMp3PlayerState
	Calculator          MaximalCalculatorState
	Text                MaximalTextState
	XmlUI               string
	CustomUIAssets      []MaximalCustomAssetState
	LuaScript           string
	LuaScriptState      string
	ContainedObjects    []MaximalObjectState
	PhysicsMaterial     MaximalPhysicsMaterialState
	Rigidbody           MaximalRigidbodyState
	JointFixed          MaximalJointFixedState
	JointHinge          MaximalJointHingeState
	JointSpring         MaximalJointSpringState
	GUID                string
	AttachedSnapPoints  []MaximalSnapPoint
	AttachedVectorLines []MaximalVectorLine
	AttachedDecals      []MaximalDecalState
	States              map[string]MaximalObjectState
	RotationValues      []MaximalRotationValueState
}
