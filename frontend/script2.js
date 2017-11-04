// Deletes the old key definition cards, and then rebuilds new o// Class for profiles.
class Profile {
    constructor(profileName, profileID, keyData) {
        this.profileName = profileName;
        this.profileID = profileID;
        this.keyData = keyData;
    }

    //Gets the evdev id of a key.
    getKeybyID(keyID){
        for(var i = 0; i<this.keyData.length; i++){
            if(keyID == this.keyData[i].EvdevID){
                return this.keyData[i];
            } 
        }
        console.log("No key found with ID of " + keyID);
        return "";
    }

    //Gets the key by its name.
    getKeybyName(keyName){
        for(var i = 0; i<this.keyData.length; i++){
            if(keyName == this.keyData[i].displayName){
                return this.keyData[i];
            }
        }
    }

    //Gets the index of a key.
    getKeyIndex(key){
        for (var i = 0; i<this.keyData.length; i++){
            if(key == this.keyData[i]){
                return i;
            }
        }
    }
}

// Class for keys.
class Key {
    constructor(displayName, mappedEvdevName, evdevName) {
        this.displayName = displayName;
        this.evdevName = evdevName;
        this.EvdevID = getEvdevID(this.evdevName);
        this.mappedEvdevName = mappedEvdevName;
        this.mappedEvdevID = getEvdevID(this.mappedEvdevName);
    }
}

// Class for layouts. LayoutArray format is as follows:
/*
[
    [
        ["Esc", 1],
        ["", 1],
        ["F1", 1],
        ["F2", 1],
        ["F3", 1],
        ["F4", 1],
        ["", 0.25],
        ["F5", 1],
        ["F6", 1],
        ["F7", 1],
        ["F8", 1],
        ["", 0.25],
        ["F9", 1],
        ["F10", 1],
        ["F11", 1],
        ["F12", 1],
        ["", 1],
        ["Print Screen", 1],
        ["Scroll Lock", 1],
        ["Pause", 1],
        ["", 1.5],
        ["", 1],
        ["", 1],
        ["", 1],
        ["", 1]
    ],
    [
        row2
    ]
    ...
]
*/

//Class for a layout.
class Layout {
    constructor(layoutArray, countryCode){
    this.layoutArray = layoutArray;
    this.countryCode = countryCode;
    }
}

// Some test values, as well as calls for initiating the keyboard and keycards.
var evdevIDs = [["KEY_RESERVED",0],["KEY_ESC",1],["KEY_1",2],["KEY_2",3],["KEY_3",4],["KEY_4",5],["KEY_5",6],["KEY_6",7],["KEY_7",8],["KEY_8",9],["KEY_9",10],["KEY_0",11],["KEY_MINUS",12],["KEY_EQUAL",13],["KEY_BACKSPACE",14],["KEY_TAB",15],["KEY_Q",16],["KEY_W",17],["KEY_E",18],["KEY_R",19],["KEY_T",20],["KEY_Y",21],["KEY_U",22],["KEY_I",23],["KEY_O",24],["KEY_P",25],["KEY_LEFTBRACE",26],["KEY_RIGHTBRACE",27],["KEY_ENTER",28],["KEY_LEFTCTRL",29],["KEY_A",30],["KEY_S",31],["KEY_D",32],["KEY_F",33],["KEY_G",34],["KEY_H",35],["KEY_J",36],["KEY_K",37],["KEY_L",38],["KEY_SEMICOLON",39],["KEY_APOSTROPHE",40],["KEY_GRAVE",41],["KEY_LEFTSHIFT",42],["KEY_BACKSLASH",43],["KEY_Z",44],["KEY_X",45],["KEY_C",46],["KEY_V",47],["KEY_B",48],["KEY_N",49],["KEY_M",50],["KEY_COMMA",51],["KEY_DOT",52],["KEY_SLASH",53],["KEY_RIGHTSHIFT",54],["KEY_KPASTERISK",55],["KEY_LEFTALT",56],["KEY_SPACE",57],["KEY_CAPSLOCK",58],["KEY_F1",59],["KEY_F2",60],["KEY_F3",61],["KEY_F4",62],["KEY_F5",63],["KEY_F6",64],["KEY_F7",65],["KEY_F8",66],["KEY_F9",67],["KEY_F10",68],["KEY_NUMLOCK",69],["KEY_SCROLLLOCK",70],["KEY_KP7",71],["KEY_KP8",72],["KEY_KP9",73],["KEY_KPMINUS",74],["KEY_KP4",75],["KEY_KP5",76],["KEY_KP6",77],["KEY_KPPLUS",78],["KEY_KP1",79],["KEY_KP2",80],["KEY_KP3",81],["KEY_KP0",82],["KEY_KPDOT",83],["KEY_ZENKAKUHANKAKU",85],["KEY_102ND",86],["KEY_F11",87],["KEY_F12",88],["KEY_RO",89],["KEY_KATAKANA",90],["KEY_HIRAGANA",91],["KEY_HENKAN",92],["KEY_KATAKANAHIRAGANA",93],["KEY_MUHENKAN",94],["KEY_KPJPCOMMA",95],["KEY_KPENTER",96],["KEY_RIGHTCTRL",97],["KEY_KPSLASH",98],["KEY_SYSRQ",99],["KEY_RIGHTALT",100],["KEY_LINEFEED",101],["KEY_HOME",102],["KEY_UP",103],["KEY_PAGEUP",104],["KEY_LEFT",105],["KEY_RIGHT",106],["KEY_END",107],["KEY_DOWN",108],["KEY_PAGEDOWN",109],["KEY_INSERT",110],["KEY_DELETE",111],["KEY_MACRO",112],["KEY_MUTE",113],["KEY_VOLUMEDOWN",114],["KEY_VOLUMEUP",115],["KEY_POWER",116],["KEY_KPEQUAL",117],["KEY_KPPLUSMINUS",118],["KEY_PAUSE",119],["KEY_SCALE",120],["KEY_KPCOMMA",121],["KEY_HANGEUL",122],["KEY_HANGUEL",122],["KEY_HANJA",123],["KEY_YEN",124],["KEY_LEFTMETA",125],["KEY_RIGHTMETA",126],["KEY_COMPOSE",127],["KEY_STOP",128],["KEY_AGAIN",129],["KEY_PROPS",130],["KEY_UNDO",131],["KEY_FRONT",132],["KEY_COPY",133],["KEY_OPEN",134],["KEY_PASTE",135],["KEY_FIND",136],["KEY_CUT",137],["KEY_HELP",138],["KEY_MENU",139],["KEY_CALC",140],["KEY_SETUP",141],["KEY_SLEEP",142],["KEY_WAKEUP",143],["KEY_FILE",144],["KEY_SENDFILE",145],["KEY_DELETEFILE",146],["KEY_XFER",147],["KEY_PROG1",148],["KEY_PROG2",149],["KEY_WWW",150],["KEY_MSDOS",151],["KEY_COFFEE",152],["KEY_SCREENLOCK",152],["KEY_ROTATE_DISPLAY",153],["KEY_DIRECTION",153],["KEY_CYCLEWINDOWS",154],["KEY_MAIL",155],["KEY_BOOKMARKS",156],["KEY_COMPUTER",157],["KEY_BACK",158],["KEY_FORWARD",159],["KEY_CLOSECD",160],["KEY_EJECTCD",161],["KEY_EJECTCLOSECD",162],["KEY_NEXTSONG",163],["KEY_PLAYPAUSE",164],["KEY_PREVIOUSSONG",165],["KEY_STOPCD",166],["KEY_RECORD",167],["KEY_REWIND",168],["KEY_PHONE",169],["KEY_ISO",170],["KEY_CONFIG",171],["KEY_HOMEPAGE",172],["KEY_REFRESH",173],["KEY_EXIT",174],["KEY_MOVE",175],["KEY_EDIT",176],["KEY_SCROLLUP",177],["KEY_SCROLLDOWN",178],["KEY_KPLEFTPAREN",179],["KEY_KPRIGHTPAREN",180],["KEY_NEW",181],["KEY_REDO",182],["KEY_F13",183],["KEY_F14",184],["KEY_F15",185],["KEY_F16",186],["KEY_F17",187],["KEY_F18",188],["KEY_F19",189],["KEY_F20",190],["KEY_F21",191],["KEY_F22",192],["KEY_F23",193],["KEY_F24",194],["KEY_PLAYCD",200],["KEY_PAUSECD",201],["KEY_PROG3",202],["KEY_PROG4",203],["KEY_DASHBOARD",204],["KEY_SUSPEND",205],["KEY_CLOSE",206],["KEY_PLAY",207],["KEY_FASTFORWARD",208],["KEY_BASSBOOST",209],["KEY_PRINT",210],["KEY_HP",211],["KEY_CAMERA",212],["KEY_SOUND",213],["KEY_QUESTION",214],["KEY_EMAIL",215],["KEY_CHAT",216],["KEY_SEARCH",217],["KEY_CONNECT",218],["KEY_FINANCE",219],["KEY_SPORT",220],["KEY_SHOP",221],["KEY_ALTERASE",222],["KEY_CANCEL",223],["KEY_BRIGHTNESSDOWN",224],["KEY_BRIGHTNESSUP",225],["KEY_MEDIA",226],["KEY_SWITCHVIDEOMODE",227],["KEY_KBDILLUMTOGGLE",228],["KEY_KBDILLUMDOWN",229],["KEY_KBDILLUMUP",230],["KEY_SEND",231],["KEY_REPLY",232],["KEY_FORWARDMAIL",233],["KEY_SAVE",234],["KEY_DOCUMENTS",235],["KEY_BATTERY",236],["KEY_BLUETOOTH",237],["KEY_WLAN",238],["KEY_UWB",239],["KEY_UNKNOWN",240],["KEY_VIDEO_NEXT",241],["KEY_VIDEO_PREV",242],["KEY_BRIGHTNESS_CYCLE",243],["KEY_BRIGHTNESS_AUTO",244],["KEY_BRIGHTNESS_ZERO",244],["KEY_DISPLAY_OFF",245],["KEY_WWAN",246],["KEY_WIMAX",246],["KEY_RFKILL",247],["KEY_MICMUTE",248]];
var layoutList = [];
layoutList[0] = new Layout([[["Esc",1],["",1],["F1",1],["F2",1],["F3",1],["F4",1],["",0.25],["F5",1],["F6",1],["F7",1],["F8",1],["",0.25],["F9",1],["F10",1],["F11",1],["F12",1],["",1],["Print",1],["ScrollLock",1],["Pause",1],["",1.5],["",1],["",1],["",1],["",1]],
    [["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],[""]],
    [["§",1,"Grave"],["1",1],["2",1],["3",1],["4",1],["5",1],["6",1],["7",1],["8",1],["9",1],["0",1],["+",1,"Minus"],["´",1,"Equal"],["<=",2,"Backspace"],["",1],["Insert",1],["Home",1],["PageUp",1],["",1],["NumLock",1],["/",1,"kpslash"],["*",1,"kpasterisk"],["kp-",1,"kpminus"],[""]],
    [["Tab",1.5],["q",1],["w",1],["e",1],["r",1],["t",1],["y",1],["u",1],["i",1],["o",1],["p",1],["å",1,"LeftBrace"],["^",1,"RightBrace"],["Enter",1.5],["",1],["Del",1,"Delete"],["End",1],["PageDown",1],["",1],["kp7",1],["kp8",1],["kp9",1],["kp+",1,"kpplus"],["",1],[""]],
    [["CapsLock",1.75],["a",1],["s",1],["d",1],["f",1],["g",1],["h",1],["j",1],["k",1],["l",1],["ö",1,"Semicolon"],["ä",1,"Apostrophe"],["'",1,"Backslash"],["",1.25],["",1],["",1],["",1],["",1],["",1],["kp4",1],["kp5",1],["kp6",1],["",1],[""]],
    [["LShift",1.25,"LeftShift"],["<",1,"102nd"],["z",1],["x",1],["c",1],["v",1],["b",1],["n",1],["m",1],[",",1,"Comma"],[".",1,"Dot"],["-",1,"Slash"],["RShift",2.9,"RightShift"],["",1],["",1],["Up",1],["",1],["",1],["kp1",1],["kp2",1],["kp3",1],["kpEnter",1],["",1],[""]],
    [["LCtrl",1.5,"LeftCtrl"],["Win",1.25,"LeftMeta"],["LAlt",1.25,"LeftAlt"],["Space",7],["RAlt",1.25,"RightAlt"],["Win",1.25,"RightMeta"],["Menu",1.25],["RCtrl",1.25,"RightCtrl"],["",1],["Left",1],["Down",1],["Right",1],["",1],["kp0",2.2],["kp,",1,"kpdot"],["",1],["",1],["",1]
    ]],"Fin");
var chosenLayout = layoutList[0];
var kbProfiles = [];
kbProfiles[0] = new Profile("Profile-0", 0, []);
var chosenProfile = kbProfiles[0];
initializeProfiles();
var chosenKey = "";
initiateKeyboard();
addProfilecards();
changeProfile(0,document.getElementById("profile-" + kbProfiles[0].profileID));

// Builds the visualized keyboard based on an array. Array has rows of keys, with each key containing two values - the displayed characters and the width in relation to a "normal" key.
function initiateKeyboard() {
    var k = 0;
    for (var i = 0; i < chosenLayout.layoutArray.length; i++) {
            var rowwrapper = document.createElement("div"); // Creating a wrapper for a row of keys
            rowwrapper.className = "rowwrapper";
            rowwrapper.id = "row-" + i;
        for (var j = 0; j < chosenLayout.layoutArray[i].length; j++) { // Creating wrappers for the buttons on the row, and then populating them with buttons created based on the chosen layouts array on the corresponding row.
            var buttonwrapper = document.createElement("div");
            buttonwrapper.className = "buttonwrapper";
            buttonwrapper.id = "wrapper-" + chosenLayout.layoutArray[i][j][0];
            var keybutton = document.createElement("button");
            keybutton.className = "keybutton";
            keybutton.id = "button-" + chosenLayout.layoutArray[i][j][0];
            if (chosenLayout.layoutArray[i][j][0] != "") {
                keybutton.setAttribute("keyName", chosenLayout.layoutArray[i][j][0]);
                k++;
            }
            // Adding listeners to the buttons as they are created.
            keybutton.addEventListener("click", function() {
                modifyKey(this.getAttribute("keyName"));
            }, false);
            // If the name of the key contains "kp", we remove the "kp" in the display but keep it in data.
            if (chosenLayout.layoutArray[i][j][0].includes("kp")) {
                keybutton.textContent = chosenLayout.layoutArray[i][j][0].replace("kp", "");
            } else {
                keybutton.textContent = chosenLayout.layoutArray[i][j][0];
            }
            // If the key has empty string in it, it is not displayed.
            if (keybutton.textContent === "") keybutton.style.display = "none";
            // Parsing the width of the key.
            var newwidth = chosenLayout.layoutArray[i][j][1] * parseInt(30);
            newwidth = newwidth + "px";
            buttonwrapper.style.width = newwidth;
            keybutton.style.width = newwidth;
            buttonwrapper.appendChild(keybutton);
            rowwrapper.appendChild(buttonwrapper);
        }
        var kbwrapper = document.getElementById("kbwrap");
        kbwrapper.appendChild(rowwrapper);
    }
    //Adds listener to the button that is used to submit changes.
    var submitBut = document.getElementById("submitchange");
    submitBut.addEventListener("click", function() {
                submitMod();
    }, false);
}

// Deletes the old key definition cards, and then rebuilds new ones. Used when changing profiles.
function addKeycards() {
    var defWrap = document.getElementById("keydefs");
    defWrap.innerHTML = "";
    for (var i = 0; i < chosenProfile.keyData.length; i++) {
        addKeycard(chosenProfile.keyData[i].displayName,chosenProfile.keyData[i].mappedEvdevName,chosenProfile.keyData[i].EvdevID);
    }
}

//Gets the evdev id of a key by name.
function getEvdevID(keyName){
    for(var i = 0; i<evdevIDs.length; i++){
        if(keyName == evdevIDs[i][0]){
            return evdevIDs[i][1];
        }
    }
    console.log(keyName + " not found!");
    return "";
}

// Adds a key definition card.
function addKeycard(keyName, mappedEvdevName, keyID) {
        var defWrap = document.getElementById("keydefs");
        var keyCard = document.createElement("div");
        keyCard.className = "card";
        keyCard.id = "keycard-" + keyName;
        keyCard.addEventListener("click", function() {
                modifyKey(this.getAttribute("keyName"));
        }, false);
        keyCard.setAttribute("keyName",keyID);
        keyCard.textContent = keyName + " - " + mappedEvdevName;Profile-3
        defWrap.appendChild(keyCard);
}

// Adds new profile cards, deleting any that had been there before.
function addProfilecards(){
    var profWrap = document.getElementById("profcards");
    profWrap.innerHTML = "";
    var addCardbutton = document.createElement("button");
    addCardbutton.className = "addbutton";
    addCardbutton.textContent = "New profile";
    addCardbutton.id = "profileadder";
    addCardbutton.addEventListener("click", function() {
    addProfile("Profile-" + parseInt(kbProfiles[kbProfiles.length-1].profileID+1),[]);
}, false);
    profWrap.appendChild(addCardbutton);
    for(var i = 0; i<kbProfiles.length; i++){
        addProfilecard(kbProfiles[i]);
    }
}

//Deletes a profile's profile card.
function deleteProfilecard(profile){
    var profileCard = document.getElementById("profile-" + profile.profileID);
    profileCard.remove();
}

//Adds a new profile and a card for it.
function addProfile(name,keydata){
    var newIndex = kbProfiles.length;
    var newID = parseInt(kbProfiles[kbProfiles.length-1].profileID)+1;
    kbProfiles[newIndex] = new Profile(name,newID,keydata);
    addProfilecard(kbProfiles[newIndex]);
}

//Deletes a profile and calls the function to delete it's card.
function deleteProfile(profile){
    if(kbProfiles.length>1 & profile!=chosenProfile){
    var profileIndex = kbProfiles.indexOf(profile);
    deleteProfilecard(profile);
    if (profileIndex > -1) {
        kbProfiles.splice(profileIndex, 1);
    }
    }
}

//Adds a profile card, which will contain a hitbox for selecting it and a button for deleting it.
function addProfilecard(profile){
    var profWrap = document.getElementById("profcards");
    var profileCard = document.createElement("div");
    var profileCardclicker = document.createElement("div");
    profileCardclicker.textContent = profile.profileName;
    profileCardclicker.className = "cardclicker";
    profileCard.className = "card";
    profileCard.id = "profile-" + profile.profileID;
    profileCard.setAttribute("profileID", profile.profileID);
    profileCardclicker.addEventListener("click", function() { //Adding a listener to the profile card.
    changeProfile(this.parentNode.getAttribute("profileID"),this.parentNode);
}, false);
    var deleteButton = document.createElement("button");
    deleteButton.className = "deletebutton";
    deleteButton.id = "delete-" + profile.profileID;
    deleteButton.setAttribute("profileID", profile.profileID);
    deleteButton.textContent = "x";
    deleteButton.addEventListener("click", function() { //Adding a listener to the button that deletes the profile.
    deleteProfile(getProfilebyID(this.getAttribute("profileID")));
}, false);
    profileCard.appendChild(profileCardclicker);
    profileCard.appendChild(deleteButton);
    profWrap.insertBefore(profileCard,document.getElementById("profileadder"));
}

// Changes the chosen profile, resetting the background color of the old chosen profile.
function changeProfile(newID, profileCard){
    var oldProfilecard = document.getElementById("profile-" + chosenProfile.profileID);
    oldProfilecard.style.backgroundColor = "";
    chosenProfile = getProfilebyID(newID);
    profileCard.style.backgroundColor = "green";
    addKeycards();
    modifyKey("");
    document.getElementById("ainput").textContent = JSON.stringify(chosenProfile, null, 4);
}

// When a key is chosen on the visualized keyboard, this is fired. It updates the chosen key and highlights the keycard, as well as removes any older highlights.
function modifyKey(keyName) {
    var keyfield = document.getElementById("keyfield");
    if(chosenProfile.getKeybyName(keyName) !== undefined) var keyid = chosenProfile.getKeybyName(keyName).EvdevID;
    if (document.getElementById("keycard-" + chosenKey) !== null){
        document.getElementById("keycard-" + chosenKey).style.backgroundColor = "";
        keyfield.textContent = "";
    }
    if (keyid !== undefined && keyid !== "") {
        var keyCard = document.getElementById("keycard-" + keyName);
        keyCard.style.backgroundColor = "green";
    }
    chosenKey = keyName;
    keyfield.textContent = keyName.replace("kp", "") + ":";
}

//Deletes a key definition from the keydata, since we don't need "unmodifieds" - it's unnecessary information.
function deleteKey(key){
var keyCard = document.getElementById("keycard-" + key.displayName);
keyCard.parentElement.removeChild(keyCard);
var indexToremove = chosenProfile.getKeyIndex(key);
chosenProfile.keyData.splice(indexToremove,1);
}

// A function for submitting a change to the key.
function submitMod() {
    if(chosenKey!==""){
    if(chosenProfile.getKeybyName(chosenKey) === undefined){
        chosenProfile.keyData[chosenProfile.keyData.length] = new Key(chosenKey,getRealname(chosenKey),getRealname(chosenKey));
        addKeycard(chosenKey,getRealname(chosenKey),chosenProfile.keyData[chosenProfile.keyData.length-1]);
        modifyKey(chosenKey);
    }
    var mapping = document.getElementById("inputmod").value;
    var chosenKeylocal = chosenProfile.getKeybyName(chosenKey);
    chosenKeylocal.mappedEvdevName = parseMapping(mapping, chosenKeylocal);
    chosenKeylocal.mappedEvdevID = parseEvdevName(chosenKeylocal.mappedEvdevName);
    document.getElementById("keycard-" + chosenKey).textContent = chosenKeylocal.displayName + " - " + chosenKeylocal.mappedEvdevName;
    if(chosenKeylocal.EvdevID == chosenKeylocal.mappedEvdevID){
        deleteKey(chosenKeylocal);
    }
    document.getElementById("ainput").textContent = JSON.stringify(chosenProfile, null, 4);
//    postKeys(chosenProfile,"/update-profile");
    }
}

function getProfilebyID(profileID){
    // Returns a profile, searched by ID.
    for(var i = 0; i<kbProfiles.length; i++){
        if(profileID == kbProfiles[i].profileID){
            return kbProfiles[i];
        }
    }
    console.log("Profile with ID of " + profileID + " not found!");
    return;
}

//Parses the string sent from submit, splitting it at designated char and then searching for the 'real names' or 'evdev names' of the mapped keystrokes, returning the resulting string of all those names.
function parseMapping(mapping, chosenKeylocal){
    if(mapping.includes(":")){var mappingArray = mapping.split(":")} else {var mappingArray = []; mappingArray[0] = mapping;};
    var realnameString = "";
    for(var i = 0; i<mappingArray.length; i++){
    if(getRealname(mappingArray[i])===undefined || mappingArray[i]===""){
        alert("Invalid input with " + mappingArray[i] + "!");
        return chosenKeylocal.mappedEvdevName;
    } else {
        if(realnameString!==""){
        realnameString = realnameString + " " + getRealname(mappingArray[i]);
        } else {
            realnameString = getRealname(mappingArray[i]);
        }
    }
    }
    return realnameString;
}

//Searches the layout profile for the keys, in case of layout issues.
function getRealname(input){
    for(var i = 0; i<chosenLayout.layoutArray.length; i++){
        for(var j = 0; j<chosenLayout.layoutArray[i].length; j++){
            if(input.toUpperCase() == chosenLayout.layoutArray[i][j][0].toUpperCase() && typeof chosenLayout.layoutArray[i][j][2] !== 'undefined'){return "KEY_" + chosenLayout.layoutArray[i][j][2].toUpperCase()} else if(input.toUpperCase() == chosenLayout.layoutArray[i][j][0].toUpperCase()) {return "KEY_" + chosenLayout.layoutArray[i][j][0].toUpperCase()};
        }
    }
    for(var i = 0; i<evdevIDs.length; i++){
        if(evdevIDs[i][0] == input){
            return evdevIDs[i][0];
        }    function loadXMLDoc(myurl) {
    }
}

//Parses the evdev name, returning any and all evdev ids.
function parseEvdevName(input){
    if(input.includes(" ")){var mappingArray = input.split(" ")} else {var mappingArray = []; mappingArray[0] = input;};
    var realidString = "";
    for(var i = 0; i<mappingArray.length; i++){
        if(realidString!==""){
        realidString = realidString + " " + getEvdevID(mappingArray[i]);
        } else {
            realidString = getEvdevID(mappingArray[i]);
        }
    }
    return realidString;
}

//Posts the JSON to server.
function postKeys(data,urli) {
      var postRequest = new XMLHttpRequest();
      postRequest.open("POST", urli, true);
      postRequest.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
      postRequest.send(JSON.stringify(data));
      postRequest.onloadend = function () {
      };
}

//Prototype to load a profile
function initializeProfiles(){
    var profileJson = geProfile("/json.api");
    profileJson = JSON.parse(profileJson);
    chosenProfile = new Profile(profileJson.profileName,profileJson.profileID,[]);
    for(var i = 0; i<profileJson.keyData.length; i++){
        chosenProfile.keyData[i] = new Key(profileJson.keyData.displayName,profileJson.keyData.mappedEvdevName,profileJson.keyData.evdevName);
    }
}


//Gets profile from the url
function getProfile(url){
        var xmlhttp;
        if (window.XMLHttpRequest) {
            xmlhttp = new XMLHttpRequest();
        } else {
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
    
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
                return xmlhttp.responseText;
            }
        }
    
        xmlhttp.open("GET", myurl, false);
        xmlhttp.send();
        return xmlhttp.onreadystatechange();
}