package main

type CubeCobraResponse struct {
	DefaultSorts     []string            `json:"defaultSorts"`
	Following        []string            `json:"following"`
	ShortId          string              `json:"shortId"`
	DefaultFormat    int                 `json:"defaultFormat"`
	Visibility       string              `json:"visibility"`
	ImageName        string              `json:"imageName"`
	Name             string              `json:"name"`
	Date             int                 `json:"date"`
	DefaultStatus    string              `json:"defaultStatus"`
	ShowUnsorted     bool                `json:"showUnsorted"`
	Keywords         []string            `json:"keywords"`
	Owner            CubeCobraUser       `json:"owner"`
	Id               string              `json:"id"`
	PriceVisibility  string              `json:"priceVisibility"`
	Featured         bool                `json:"featured"`
	Tags             []string            `json:"tags"`
	CardCount        int                 `json:"cardCount"`
	CategoryOverride string              `json:"categoryOverride"`
	NumDecks         int                 `json:"numDecks"`
	TagColors        []CubeCobraTagColor `json:"tagColors"`
	Basics           []string            `json:"basics"`
	DefaultPrinting  string              `json:"defaultPrinting"`
	DisableAlerts    bool                `json:"disableAlerts"`
	Formats          []CubeCobraFormat   `json:"formats"`
	Description      string              `json:"description"`
	CategoryPrefixes []string            `json:"categoryPrefixes"`
	Image            CubeCobraUserImage  `json:"image"`
	Cards            CubeCobraCardsEntry `json:"cards"`
}

type CubeCobraUser struct {
	Following     []string           `json:"following"`
	Theme         string             `json:"theme"`
	HideFeatured  bool               `json:"hideFeatured"`
	FollowedCubes string             `json:"followedCubes"`
	ImageName     string             `json:"imageName"`
	FollowedUsers []string           `json:"followedUsers"`
	Roles         []string           `json:"roles"`
	UsernameLower string             `json:"usernameLower"`
	About         string             `json:"about"`
	Image         CubeCobraUserImage `json:"image"`
	HideTagColors bool               `json:"hideTagColors"`
	Username      string             `json:"username"`
	Id            string             `json:"id"`
	Patron        string             `json:"patron"`
}

type CubeCobraUserImage struct {
	Uri       string `json:"uri"`
	Artist    string `json:"artist"`
	Id        string `json:"id"`
	ImageName string `json:"imageName"`
}

type CubeCobraTagColor struct {
	Color string `json:"color"`
	Tag   string `json:"tag"`
}

type CubeCobraFormat struct {
	Markdown  string `json:"markdown"`
	Title     string `json:"title"`
	Packs     []any  `json:"packs"`
	Multiples bool   `json:"multiples"`
}

type CubeCobraCardsEntry struct {
	Id         string          `json:"id"`
	Mainboard  []CubeCobraCard `json:"mainboard"`
	Maybeboard []CubeCobraCard `json:"maybeboard"`
}

type CubeCobraCard struct {
	CardID    string               `json:"cardID"`
	AddedTmsp int                  `json:"addedTmsp"`
	Status    string               `json:"status"`
	Details   CubeCobraCardDetails `json:"details"`
	Index     int                  `json:"index"`
	Board     string               `json:"board"`
}

type CubeCobraCardDetails struct {
	Elo              float32  `json:"elo"`
	Popularity       float32  `json:"popularity"`
	CubeCount        int      `json:"cubeCount"`
	PickCount        int      `json:"pickCount"`
	IsExtra          bool     `json:"isExtra"`
	Color_identity   []string `json:"color_identity"`
	Set              string   `json:"set"`
	Set_name         string   `json:"set_name"`
	Finishes         []string `json:"finishes"`
	Collector_number string   `json:"collector_number"`
	Released_at      string   `json:"released_at"`
	Reprint          bool     `json:"reprint"`
	Promo            bool     `json:"promo"`
	Prices           struct {
		Usd        float32 `json:"usd"`
		Usd_foil   float32 `json:"usd_foil"`
		Usd_etched float32 `json:"usd_etched"`
		Eur        float32 `json:"eur"`
		Tix        float32 `json:"tix"`
	} `json:"prices"`
	Digital      bool   `json:"digital"`
	IsToken      bool   `json:"isToken"`
	Border_color string `json:"border_color"`
	Name         string `json:"name"`
	Name_lower   string `json:"name_lower"`
	Full_name    string `json:"full_name"`
	Artist       string `json:"artist"`
	Scryfall_uri string `json:"scryfall_uri"`
	Rarity       string `json:"rarity"`
	Oracle_text  string `json:"oracle_text"`
	Scryfall_id  string `json:"scryfall_id"`
	Oracle_id    string `json:"oracle_id"`
	Cmc          int    `json:"cmc"`
	Legalities   struct {
		Legacy    string `json:"legacy"`
		Modern    string `json:"modern"`
		Standard  string `json:"standard"`
		Pioneer   string `json:"pioneer"`
		Pauper    string `json:"pauper"`
		Brawl     string `json:"brawl"`
		Historic  string `json:"historic"`
		Commander string `json:"commander"`
		Penny     string `json:"penny"`
		Vintage   string `json:"vintage"`
	} `json:"legalities"`
	Parsed_cost   []string `json:"parsed_cost"`
	Colors        []string `json:"colors"`
	Type          string   `json:"type"`
	Full_art      string   `json:"full_art"`
	Language      string   `json:"language"`
	Mtgo_id       int      `json:"mtgo_id"`
	Layout        string   `json:"layout"`
	Tcgplayer_id  int      `json:"tcgplayer_id"`
	Power         string   `json:"power"`
	Toughness     string   `json:"toughness"`
	Image_small   string   `json:"image_small"`
	Image_normal  string   `json:"image_normal"`
	Art_crop      string   `json:"art_crop"`
	ColorCategory string   `json:"colorCategory"`
}
