// Class for profiles.
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
        createNotification("No key found with ID of " + keyID,true);
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
        this.EvdevID = parseEvdevName(this.evdevName);
        this.mappedEvdevName = mappedEvdevName;
        this.mappedEvdevID = parseEvdevName(this.mappedEvdevName);
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
    constructor(layoutArray, countryCode, realNames){
    this.layoutArray = layoutArray;
    this.countryCode = countryCode;
    this.realNames = realNames;
    }
}

// Some test values, as well as calls for initiating the keyboard and keycards.
var layoutList = [];
layoutList[0] = new Layout([[["Esc",1],["",1],["F1",1],["F2",1],["F3",1],["F4",1],["",0.25],["F5",1],["F6",1],["F7",1],["F8",1],["",0.25],["F9",1],["F10",1],["F11",1],["F12",1],["",1],["Print",1],["ScrollLock",1],["Pause",1],["",1.5],["",1],["",1],["",1],["",1]],
    [["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],[""]],
    [["§",1,"Grave"],["1",1],["2",1],["3",1],["4",1],["5",1],["6",1],["7",1],["8",1],["9",1],["0",1],["+",1,"Minus"],["´",1,"Equal"],["Backspace",2],["",1],["Insert",1],["Home",1],["PageUp",1],["",1],["NumLock",1],["/",1,"kpslash"],["*",1,"kpasterisk"],["kp-",1,"kpminus"],[""]],
    [["Tab",1.5],["q",1],["w",1],["e",1],["r",1],["t",1],["y",1],["u",1],["i",1],["o",1],["p",1],["å",1,"LeftBrace"],["^",1,"RightBrace"],["Enter",1.5],["",1],["Del",1,"Delete"],["End",1],["PageDown",1],["",1],["kp7",1],["kp8",1],["kp9",1],["kp+",1,"kpplus"],["",1],[""]],
    [["CapsLock",1.75],["a",1],["s",1],["d",1],["f",1],["g",1],["h",1],["j",1],["k",1],["l",1],["ö",1,"Semicolon"],["ä",1,"Apostrophe"],["'",1,"Backslash"],["",1.25],["",1],["",1],["",1],["",1],["",1],["kp4",1],["kp5",1],["kp6",1],["",1],[""]],
    [["LShift",1.25,"LeftShift"],["<",1,"102nd"],["z",1],["x",1],["c",1],["v",1],["b",1],["n",1],["m",1],[",",1,"Comma"],[".",1,"Dot"],["-",1,"Slash"],["RShift",2.9,"RightShift"],["",1],["",1],["Up",1],["",1],["",1],["kp1",1],["kp2",1],["kp3",1],["kpEnter",1],["",1],[""]],
    [["LCtrl",1.5,"LeftCtrl"],["Win",1.25,"LeftMeta"],["LAlt",1.25,"LeftAlt"],[" ",7,"Space"],["RAlt",1.25,"RightAlt"],["RWin",1.25,"RightMeta"],["Compose",1.25],["RCtrl",1.25,"RightCtrl"],["",1],["Left",1],["Down",1],["Right",1],["",1],["kp0",2.2],["kp,",1,"kpdot"],["",1],["",1],["",1]
    ]],"Fin",true);
var chosenLayout = layoutList[0];
var kbProfiles = [];
var chosenProfile;
kbProfiles[0] = chosenProfile;
var chosenKey = "";
var heatmapModeOn = false;
var oldactive = 1;
var currheatmap = "";

//Executes function calls when the page is loaded.
window.onload = function() {
    loadProfiles();
    initiateKeyboard();
    addProfilecards();
    changeProfile(kbProfiles[0].profileID,document.getElementById("profile-" + kbProfiles[0].profileID));
    var getActive = setInterval(function(){
    refreshActiveprofile();
    },3000);
    createHelp("Basics",'In order to map keys, you must first choose a key from the visualized keyboard and then input the new key def to the textbox at bottom. Use the keynames shown on the visualized keyboard, or alternatively, EVDEV-names. For simultaneous keystrokes, separate keys with :. For separate strokes, use |. You can chain these if you want - examples: k:i:s:s:a, k:i:s:s:a|k|i|s|s|a, a:b:c|c:b:a.',1);
    createHelp("Submitting your changes",'To submit changes, simply press enter while the text field is active, or alternatively press the "Submit" or "Post" button.',5)
    createHelp("Deleting and editing",'You can delete profiles and keydefs by clicking the "x" buttons. Defining a key to the original value will also delete the definition. You can change the profile names with the edit buttons on the tags, and you can re-edit a key by either normally selecting it from the board or selecting the key definition card.',6);
    createHelp("Defining a profile change button",'A normal change: Mode("Profile name"/Profile ID,true) or Profiles("Profile name"/Profile ID,true). A shift type change: Mode("Profile name"/Profile ID) or Profiles("Profile name"/Profile ID,true).',7)
    createHelp("Commands",'For quickly defining a string with no special symbols to a key, use write("string"). To repeat something, use repeat("",count) - if you wish to do separate reports inside repeat, use > instead of |. To insert delays, use delay(seconds). To define a key that changes a profile, use Profiles("Profile-2") or with profile-IDs Profiles("2"). You may use either profile names or IDs. To define a mode change button, use Mode("Profile-1/1",booleanfortoggle).',2);
    createHelp("Connectors, TL;DR","a|b - Separate reports. a:b - Same report. $number - delay.",3)
    createHelp("Commands, TL;DR",'write(""),w(""),repeat("",int),delay(number),Profiles(int/string),Mode(int/string,bool)',4);
    createHelp("Heatmaps",'You can toggle either a long term heatmap or temporary heatmap. Temporary heatmaps will not be saved and will only connect data until you reset it. The long term heatmap requires file removal to be reset, as it is supposed to be the all-time data.',8);
    createHelp("Display mode",'The display mode toggle toggles between original names on the visualized keyboard and the mapped definitions.',9);
};

function createHelp(helpname,helptext,helpid){
var wrapperdiv = document.createElement("div");
var clickdiv = document.createElement("button");
clickdiv.className = "helpclicker closed";
clickdiv.setAttribute("helpID",helpid);
clickdiv.textContent = helpname;
clickdiv.addEventListener("click",function(){
document.getElementById(this.getAttribute("helpID")).classList.toggle("hidden");
this.classList.toggle("closed");
this.classList.toggle("open");
},false)
var textcontainer = document.createElement("div");
textcontainer.className = "helptext hidden";
textcontainer.textContent = helptext;
textcontainer.id = helpid;
wrapperdiv.appendChild(clickdiv);
wrapperdiv.appendChild(textcontainer);
document.getElementById("helpbox").appendChild(wrapperdiv);
}

// Builds the visualized keyboard based on an array. Array has rows of keys, with each key containing two values - the displayed characters and the width in relation to a "normal" key.
function initiateKeyboard() {
    var k = 0;
    for (var i = 0; i < chosenLayout.layoutArray.length; i++) {
        var rowwrapper = document.createElement("div"); // Creating a wrapper for a row of keys
        rowwrapper.className = "rowwrapper";
        rowwrapper.id = "row-" + i;
        for (var j = 0; j < chosenLayout.layoutArray[i].length; j++) { // Creating wrappers for the buttons on the row, and then populating them with buttons created based on the chosen layouts array on the corresponding row.
            var buttonwrapper = document.createElement("div");
            var textDiv = document.createElement("div");
            textDiv.className = "buttonhelp";
            textDiv.id = "buttonhelp-" + chosenLayout.layoutArray[i][j][0];
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
                document.getElementById("button-" + chosenKey).classList.remove("chosen");
                this.classList.add("chosen");
                modifyKey(this.getAttribute("keyName"));
            }, false);

            keybutton.addEventListener("mouseenter", function( event ) {   
                event.target.style.borderWidth = "3px";
                if(chosenProfile.getKeybyName(this.getAttribute("keyName")) === undefined){
                document.getElementById("buttonhelp-" + this.getAttribute("keyName")).textContent = "Mapped as: " + this.getAttribute("keyName");
                } else {
                if(chosenProfile.getKeybyName(this.getAttribute("keyName")).mappedEvdevName !== undefined){
                document.getElementById("buttonhelp-" + this.getAttribute("keyName")).textContent = "Mapped as: " + chosenProfile.getKeybyName(this.getAttribute("keyName")).mappedEvdevName.replace(/KEY_/g,"").toLowerCase();
                } else if (chosenProfile.getKeybyName(this.getAttribute("keyName")).toggle === true) {
                document.getElementById("buttonhelp-" + this.getAttribute("keyName")).textContent = "Toggle profile: " + getProfilebyID(chosenProfile.getKeybyName(this.getAttribute("keyName")).profiles[0]).profileName;                    
                } else {
                document.getElementById("buttonhelp-" + this.getAttribute("keyName")).textContent = "Switch profile: " + getProfilebyID(chosenProfile.getKeybyName(this.getAttribute("keyName")).profiles[0]).profileName;                    
                }
            }
                document.getElementById("buttonhelp-" + this.getAttribute("keyName")).style.display = "block";                
                document.getElementById("buttonhelp-" + this.getAttribute("keyName")).style.opacity = 1;
                setTimeout(function() {
                event.target.style.borderWidth = "";
                }, 500);
              }, false);

              keybutton.addEventListener("mouseout", function( event ) {
                document.getElementById("buttonhelp-" + this.getAttribute("keyName")).style.opacity = 0;
                document.getElementById("buttonhelp-" + this.getAttribute("keyName")).style.display = "";     
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
            buttonwrapper.appendChild(textDiv);
            rowwrapper.appendChild(buttonwrapper);
        }
        var kbwrapper = document.getElementById("kbwrap");
        kbwrapper.appendChild(rowwrapper);
    }
    var form = document.getElementById("submitForm");

    form.addEventListener('submit', handleForm);
}

//Function to get a list of all the evdev ids and names paired together.
function getAllEvdevIDs() {
    var evdevIDs = [["KEY_RESERVED",0],["KEY_ESC",1],["KEY_1",2],["KEY_2",3],["KEY_3",4],["KEY_4",5],["KEY_5",6],["KEY_6",7],["KEY_7",8],["KEY_8",9],["KEY_9",10],["KEY_0",11],["KEY_MINUS",12],["KEY_EQUAL",13],["KEY_BACKSPACE",14],["KEY_TAB",15],["KEY_Q",16],["KEY_W",17],["KEY_E",18],["KEY_R",19],["KEY_T",20],["KEY_Y",21],["KEY_U",22],["KEY_I",23],["KEY_O",24],["KEY_P",25],["KEY_LEFTBRACE",26],["KEY_RIGHTBRACE",27],["KEY_ENTER",28],["KEY_LEFTCTRL",29],["KEY_A",30],["KEY_S",31],["KEY_D",32],["KEY_F",33],["KEY_G",34],["KEY_H",35],["KEY_J",36],["KEY_K",37],["KEY_L",38],["KEY_SEMICOLON",39],["KEY_APOSTROPHE",40],["KEY_GRAVE",41],["KEY_LEFTSHIFT",42],["KEY_BACKSLASH",43],["KEY_Z",44],["KEY_X",45],["KEY_C",46],["KEY_V",47],["KEY_B",48],["KEY_N",49],["KEY_M",50],["KEY_COMMA",51],["KEY_DOT",52],["KEY_SLASH",53],["KEY_RIGHTSHIFT",54],["KEY_KPASTERISK",55],["KEY_LEFTALT",56],["KEY_SPACE",57],["KEY_CAPSLOCK",58],["KEY_F1",59],["KEY_F2",60],["KEY_F3",61],["KEY_F4",62],["KEY_F5",63],["KEY_F6",64],["KEY_F7",65],["KEY_F8",66],["KEY_F9",67],["KEY_F10",68],["KEY_NUMLOCK",69],["KEY_SCROLLLOCK",70],["KEY_KP7",71],["KEY_KP8",72],["KEY_KP9",73],["KEY_KPMINUS",74],["KEY_KP4",75],["KEY_KP5",76],["KEY_KP6",77],["KEY_KPPLUS",78],["KEY_KP1",79],["KEY_KP2",80],["KEY_KP3",81],["KEY_KP0",82],["KEY_KPDOT",83],["KEY_ZENKAKUHANKAKU",85],["KEY_102ND",86],["KEY_F11",87],["KEY_F12",88],["KEY_RO",89],["KEY_KATAKANA",90],["KEY_HIRAGANA",91],["KEY_HENKAN",92],["KEY_KATAKANAHIRAGANA",93],["KEY_MUHENKAN",94],["KEY_KPJPCOMMA",95],["KEY_KPENTER",96],["KEY_RIGHTCTRL",97],["KEY_KPSLASH",98],["KEY_SYSRQ",99],["KEY_RIGHTALT",100],["KEY_LINEFEED",101],["KEY_HOME",102],["KEY_UP",103],["KEY_PAGEUP",104],["KEY_LEFT",105],["KEY_RIGHT",106],["KEY_END",107],["KEY_DOWN",108],["KEY_PAGEDOWN",109],["KEY_INSERT",110],["KEY_DELETE",111],["KEY_MACRO",112],["KEY_MUTE",113],["KEY_VOLUMEDOWN",114],["KEY_VOLUMEUP",115],["KEY_POWER",116],["KEY_KPEQUAL",117],["KEY_KPPLUSMINUS",118],["KEY_PAUSE",119],["KEY_SCALE",120],["KEY_KPCOMMA",121],["KEY_HANGEUL",122],["KEY_HANGUEL",122],["KEY_HANJA",123],["KEY_YEN",124],["KEY_LEFTMETA",125],["KEY_RIGHTMETA",126],["KEY_COMPOSE",127],["KEY_STOP",128],["KEY_AGAIN",129],["KEY_PROPS",130],["KEY_UNDO",131],["KEY_FRONT",132],["KEY_COPY",133],["KEY_OPEN",134],["KEY_PASTE",135],["KEY_FIND",136],["KEY_CUT",137],["KEY_HELP",138],["KEY_MENU",139],["KEY_CALC",140],["KEY_SETUP",141],["KEY_SLEEP",142],["KEY_WAKEUP",143],["KEY_FILE",144],["KEY_SENDFILE",145],["KEY_DELETEFILE",146],["KEY_XFER",147],["KEY_PROG1",148],["KEY_PROG2",149],["KEY_WWW",150],["KEY_MSDOS",151],["KEY_COFFEE",152],["KEY_SCREENLOCK",152],["KEY_ROTATE_DISPLAY",153],["KEY_DIRECTION",153],["KEY_CYCLEWINDOWS",154],["KEY_MAIL",155],["KEY_BOOKMARKS",156],["KEY_COMPUTER",157],["KEY_BACK",158],["KEY_FORWARD",159],["KEY_CLOSECD",160],["KEY_EJECTCD",161],["KEY_EJECTCLOSECD",162],["KEY_NEXTSONG",163],["KEY_PLAYPAUSE",164],["KEY_PREVIOUSSONG",165],["KEY_STOPCD",166],["KEY_RECORD",167],["KEY_REWIND",168],["KEY_PHONE",169],["KEY_ISO",170],["KEY_CONFIG",171],["KEY_HOMEPAGE",172],["KEY_REFRESH",173],["KEY_EXIT",174],["KEY_MOVE",175],["KEY_EDIT",176],["KEY_SCROLLUP",177],["KEY_SCROLLDOWN",178],["KEY_KPLEFTPAREN",179],["KEY_KPRIGHTPAREN",180],["KEY_NEW",181],["KEY_REDO",182],["KEY_F13",183],["KEY_F14",184],["KEY_F15",185],["KEY_F16",186],["KEY_F17",187],["KEY_F18",188],["KEY_F19",189],["KEY_F20",190],["KEY_F21",191],["KEY_F22",192],["KEY_F23",193],["KEY_F24",194],["KEY_PLAYCD",200],["KEY_PAUSECD",201],["KEY_PROG3",202],["KEY_PROG4",203],["KEY_DASHBOARD",204],["KEY_SUSPEND",205],["KEY_CLOSE",206],["KEY_PLAY",207],["KEY_FASTFORWARD",208],["KEY_BASSBOOST",209],["KEY_PRINT",210],["KEY_HP",211],["KEY_CAMERA",212],["KEY_SOUND",213],["KEY_QUESTION",214],["KEY_EMAIL",215],["KEY_CHAT",216],["KEY_SEARCH",217],["KEY_CONNECT",218],["KEY_FINANCE",219],["KEY_SPORT",220],["KEY_SHOP",221],["KEY_ALTERASE",222],["KEY_CANCEL",223],["KEY_BRIGHTNESSDOWN",224],["KEY_BRIGHTNESSUP",225],["KEY_MEDIA",226],["KEY_SWITCHVIDEOMODE",227],["KEY_KBDILLUMTOGGLE",228],["KEY_KBDILLUMDOWN",229],["KEY_KBDILLUMUP",230],["KEY_SEND",231],["KEY_REPLY",232],["KEY_FORWARDMAIL",233],["KEY_SAVE",234],["KEY_DOCUMENTS",235],["KEY_BATTERY",236],["KEY_BLUETOOTH",237],["KEY_WLAN",238],["KEY_UWB",239],["KEY_UNKNOWN",240],["KEY_VIDEO_NEXT",241],["KEY_VIDEO_PREV",242],["KEY_BRIGHTNESS_CYCLE",243],["KEY_BRIGHTNESS_AUTO",244],["KEY_BRIGHTNESS_ZERO",244],["KEY_DISPLAY_OFF",245],["KEY_WWAN",246],["KEY_WIMAX",246],["KEY_RFKILL",247],["KEY_MICMUTE",248]];
    return evdevIDs;    
}

function handleForm(event) { event.preventDefault(); }

// Deletes the old key definition cards, and then rebuilds new ones. Used when changing profiles.
function addKeycards() {
    var defWrap = document.getElementById("keydefs");
    defWrap.innerHTML = "";
    for (var i = 0; i < chosenProfile.keyData.length; i++) {
        addKeycard(chosenProfile.keyData[i].displayName, chosenProfile.keyData[i].mappedEvdevName, chosenProfile.keyData[i].EvdevID);
    }
}

//Gets the evdev id of a key by name.
function getEvdevID(keyName) {
    var evdevIDs = getAllEvdevIDs();
    for (var i = 0; i < evdevIDs.length; i++) {
        if (keyName == evdevIDs[i][0]) {
            return evdevIDs[i][1];
        }
    }
    createNotification(keyName + " not found!",true);
    return "";
}

// Adds a key definition card.
function addKeycard(keyName, mappedEvdevName, keyID) {
    var defWrap = document.getElementById("keydefs");
    var keyCard = document.createElement("div");
    var textCard = document.createElement("div");
    textCard.id = "keycard-" + keyName + "-text";
    textCard.className = "textWrap";
    keyCard.className = "card";
    keyCard.id = "keycard-" + keyName;
    keyCard.addEventListener("click", function() {
        document.getElementById("button-" + chosenKey).classList.remove("chosen");
        modifyKey(this.getAttribute("keyName"));
        document.getElementById("button-" + chosenKey).classList.add("chosen");
    }, false);
    keyCard.setAttribute("keyName", keyName);
    
 //   if(chosenProfile.getKeybyName(keyName).profiles !== undefined) textCard.textContent = keyName + " - " + "Profiles: " + chosenProfile.getKeybyName(keyName).profiles;

                if (chosenProfile.getKeybyName(keyName).toggle === true) {
                textCard.textContent = keyName + " - " + "Toggle profile: " + getProfilebyID(chosenProfile.getKeybyName(keyName).profiles[0]).profileName;                    
                } else if (chosenProfile.getKeybyName(keyName).toggle === false) {
                textCard.textContent = keyName + " - " + "Switch profile: " + getProfilebyID(chosenProfile.getKeybyName(keyName).profiles[0]).profileName;                    
                } else {
                    textCard.textContent = keyName + " - " + chosenProfile.getKeybyName(keyName).mappedEvdevName.replace(/KEY_/g,"").toLowerCase();
                }

    var deleteButton = document.createElement("button");
    deleteButton.className = "deletebutton";
    deleteButton.id = "delete-" + keyName;
    deleteButton.setAttribute("keyName", keyName);
    deleteButton.textContent = "x";
    deleteButton.addEventListener("click", function() { //Adding a listener to the button that deletes the profile.
        deleteKey(chosenProfile.getKeybyName((this.getAttribute("keyName"))));
        document.getElementById("button-" + chosenKey).classList.remove("chosen");
    }, false);
    keyCard.appendChild(textCard);
    keyCard.appendChild(deleteButton);
    defWrap.appendChild(keyCard);
}

//Toggles the display mode for buttons.
function toggleDisplaymode(notify) {
    chosenLayout.realNames = !chosenLayout.realNames;
    if(chosenLayout.realNames == true && notify!==false) {
        createNotification("Using original names!");
    } else if(notify!==false) {
        createNotification("Using mapped names!");
    }
    for (var i = 0; i < chosenLayout.layoutArray.length; i++) {
        for (var j = 0; j < chosenLayout.layoutArray[i].length; j++) {
                var button = document.getElementById("button-" + chosenLayout.layoutArray[i][j][0]);
                if (chosenLayout.realNames === false && chosenProfile.getKeybyName(chosenLayout.layoutArray[i][j][0]) !== undefined) {
                    if(chosenProfile.getKeybyName(chosenLayout.layoutArray[i][j][0]).mappedEvdevName !== undefined){
                    var getLayoutnameinput = chosenProfile.getKeybyName(chosenLayout.layoutArray[i][j][0]).mappedEvdevName;
                    getLayoutnameinput = getLayoutnameinput.replace(/KEY_/g, "").toLowerCase();;
                    button.textContent = getLayoutnameinput.toLowerCase();
                    } else {
                    var getLayoutnameinput = "Profile: " + chosenProfile.getKeybyName(chosenLayout.layoutArray[i][j][0]).profiles;
                    button.textContent = getLayoutnameinput;
                    }
                } else if (chosenLayout.realNames === true) {
                    button.textContent = chosenLayout.layoutArray[i][j][0].replace("kp","");
                }
        }
    }
}

function refreshActiveprofile(){
    var activeID = getJson('/curprofile.api');
  // var activeID = "[1]";
    if(activeID.includes('[')) activeID = JSON.parse(activeID);
    activeID = parseInt(activeID);
    if(getProfilebyID(activeID) !== false){
    document.getElementById("profile-" + oldactive).classList.remove("activeprofile");
    document.getElementById("profile-" + activeID).classList.add("activeprofile");
    oldactive = activeID;
    }
}

//Function that shows heatmap visualization on keyboard layout
function toggleHeatmap(heatmapApi, isInterval) {
    //get heatmap statistics from json file
    if (heatmapApi !== "") {
        currheatmap = heatmapApi;
    }
    var heatmapStats = getJson(heatmapApi);
   // var heatmapStats = '{"56": 8, "15": 24, "29": 57, "30": 48, "35": 9, "18": 10, "20": 17, "108": 11, "28": 16, "42": 45, "19": 35, "45": 2, "51": 7, "47": 11, "31": 37, "72": 2, "71": 2, "77": 2, "76": 1, "2": 3, "3": 19, "4": 1, "5": 1, "57": 58, "58": 14, "33": 13, "34": 11, "9": 11, "10": 8, "7": 5, "8": 6, "105": 41, "46": 16, "14": 65, "6": 10, "12": 8, "106": 26, "36": 1, "23": 5, "25": 13, "50": 5, "24": 8, "22": 18, "49": 7, "32": 5, "52": 7, "38": 13, "43": 3, "11": 11, "53": 4, "100": 4, "48": 3, "21": 2, "37": 4, "17": 4, "63": 1, "41": 31, "86": 1, "44": 5}';
    try{
    //Parse heatmap stats in to a dict
    heatmapStats = JSON.parse(heatmapStats);
    //put heatmap
    var heatmapArray = [], heatmapStats;
    for(a in heatmapStats){
        heatmapArray.push([a,heatmapStats[a]])
       }
    heatmapArray.sort(function(a,b){return a[1] - b[1]});
    heatmapArray.reverse();

    var mostpressed = heatmapArray[0];
    var leastpressed = heatmapArray[heatmapArray.length-1];

    var heatmapIDs = [], heatmapArray;
    var heatmapTimesPressed = [], heatmapArray;
    for (a in heatmapArray){
        heatmapIDs.push(heatmapArray[a][0]);
        heatmapTimesPressed.push(heatmapArray[a][1]);
    }  

    }
    catch(err) {
        createNotification(err + "! Creating heatmap failed.", true); 
    }
   
    for (var i = 0; i < chosenLayout.layoutArray.length; i++) {
        for (var j = 0; j < chosenLayout.layoutArray[i].length; j++) {
                var button = document.getElementById("button-" + chosenLayout.layoutArray[i][j][0]);
                          
                if (chosenLayout.layoutArray[i][j][0]!== ""){
                
                if(!heatmapModeOn || isInterval){
                var comparenumber = heatmapIDs.indexOf(parseEvdevName(getRealname(chosenLayout.layoutArray[i][j][0])).toString());
                var scalar = 0;
                if (comparenumber >= 0)
                {
                scalar = heatmapTimesPressed[comparenumber] / mostpressed[1];
                var apu = 1-scalar;
                button.style.backgroundColor = "rgba(" + Math.round(scalar*255) + ",0," + Math.round(apu*255) + ",1)";
                } else {
                button.style.backgroundColor = "rgba(0,0,255,1)";
                }
                button.style.color = "white";
                button.style.boxShadow = "0px 0px " + parseInt(25 + Math.round(scalar*25)) + "px " + button.style.backgroundColor + ",0px 0px " + parseInt(25 + Math.round(scalar*25)) + "px " + button.style.backgroundColor;
            }
            else if (heatmapStats == "") {
                button.style.backgroundColor = "";
                button.style.color = "";
                button.style.boxShadow = "";
                heatmapModeOn = !heatmapModeOn;
            }

            else {
                button.style.backgroundColor = "";
                button.style.color = "";
                button.style.boxShadow = "";
            }
            }
        }
    }
    if(isInterval !== true){
        heatmapModeOn = !heatmapModeOn;
    }
    if(heatmapModeOn === true && isInterval !== true){
      var pollHeatmap =  setInterval(function(){
        if(heatmapModeOn === false){
            clearInterval(pollHeatmap);
            return;
        }
        toggleHeatmap(currheatmap, true);
        }, 5000);
    }
}


// Adds new profile cards, deleting any that had been there before.
function addProfilecards() {
    var profWrap = document.getElementById("profcards");
    profWrap.innerHTML = "";
    var addCardbutton = document.createElement("button");
    addCardbutton.className = "addbutton";
    addCardbutton.textContent = "New profile";
    addCardbutton.id = "profileadder";
    addCardbutton.addEventListener("click", function() {
        addProfile("Profile-" + parseInt(kbProfiles[kbProfiles.length - 1].profileID + 1), []);
    }, false);
    profWrap.appendChild(addCardbutton);
    for (var i = 0; i < kbProfiles.length; i++) {
        addProfilecard(kbProfiles[i]);
    }
}

//Deletes a profile's profile card.
function deleteProfilecard(profile) {
    var profileCard = document.getElementById("profile-" + profile.profileID);
    profileCard.remove();
}

//Adds a new profile and a card for it.
function addProfile(name, keydata) {
    var newIndex = kbProfiles.length;
    var newID = parseInt(kbProfiles[kbProfiles.length - 1].profileID) + 1;
    kbProfiles[newIndex] = new Profile(name, newID, keydata);
    addProfilecard(kbProfiles[newIndex]);
    document.getElementById("ainput").textContent = JSON.stringify(parsePostdata(), null, 4);
}

//Deletes a profile and calls the function to delete it's card.
function deleteProfile(profile) {
    if (kbProfiles.length > 1 & profile != chosenProfile) {
        var profileIndex = kbProfiles.indexOf(profile);
        deleteProfilecard(profile);
        if (profileIndex > -1) {
            kbProfiles.splice(profileIndex, 1);
        }
    }
    document.getElementById("ainput").textContent = JSON.stringify(parsePostdata(), null, 4);
}

//Adds a profile card, which will contain a hitbox for selecting it and a button for deleting it.
function addProfilecard(profile) {
    var profWrap = document.getElementById("profcards");
    var profileCard = document.createElement("div");
    var profileCardtext = document.createElement("div");
    profileCardtext.textContent = profile.profileName + " - ID: " + profile.profileID;
    profileCardtext.className = "cardtext";
    profileCard.className = "card";
    profileCard.id = "profile-" + profile.profileID;
    profileCard.setAttribute("profileID", profile.profileID);
    profileCard.addEventListener("click", function() { //Adding a listener to the profile card.
        document.getElementById("button-" + chosenKey).classList.remove("chosen");
        changeProfile(this.getAttribute("profileID"), this);
    }, false);
    var deleteButton = document.createElement("button");
    var editButton = document.createElement("button");
    editButton.className = "editbutton";
    deleteButton.className = "deletebutton";
    editButton.id = "edit-" + profile.profileID;
    deleteButton.id = "delete-" + profile.profileID;
    editButton.setAttribute("profileID", profile.profileID);
    editButton.textContent = "Name";
    deleteButton.setAttribute("profileID", profile.profileID);
    deleteButton.textContent = "x";
    deleteButton.addEventListener("click", function() { //Adding a listener to the button that deletes the profile.
        deleteProfile(getProfilebyID(this.getAttribute("profileID")));
    }, false);
    editButton.addEventListener("click", function() { //Adding a listener to the button that deletes the profile.
        editProfile(getProfilebyID(this.getAttribute("profileID")));
    }, false);
    profileCard.appendChild(profileCardtext);
    profileCard.appendChild(deleteButton);
    profileCard.appendChild(editButton);
    profWrap.insertBefore(profileCard, document.getElementById("profileadder"));
}

//Changes the name of the profile.
function editProfile(profile){
    var newName = prompt("Enter a new profile name!", "Profile name here.");
    if(newName!==null){
    profile.profileName = newName;
    var profileCard = document.getElementById("profile-" + profile.profileID);
    profileCard.firstChild.textContent = profile.profileName + " - ID: " + profile.profileID;
    }
}

// Changes the chosen profile, resetting the background color of the old chosen profile.
function changeProfile(newID, profileCard) {
    if(getProfilebyID(newID)!==false){
    var oldProfilecard = document.getElementById("profile-" + chosenProfile.profileID);
    oldProfilecard.style.backgroundColor = "";
    document.getElementById("button-" + chosenKey).style.backgroundColor = "";
    chosenProfile = getProfilebyID(newID);
    profileCard.style.backgroundColor = "rgba(40,40,40,0.5)";
    addKeycards();
    modifyKey("");
    document.getElementById("ainput").textContent = JSON.stringify(parsePostdata(), null, 4);
    toggleDisplaymode(false);
    toggleDisplaymode(false);
    }
}

// When a key is chosen on the visualized keyboard, this is fired. It updates the chosen key and highlights the keycard, as well as removes any older highlights.
function modifyKey(keyName) {
    var keyfield = document.getElementById("keyfield");
    if (chosenProfile.getKeybyName(keyName) !== undefined) var keyid = chosenProfile.getKeybyName(keyName).EvdevID;
    if (document.getElementById("keycard-" + chosenKey) !== null) {
        document.getElementById("keycard-" + chosenKey).style.backgroundColor = "";
        keyfield.textContent = "";
    }
    if (keyid !== undefined && keyid !== "") {
        var keyCard = document.getElementById("keycard-" + keyName);
        keyCard.style.backgroundColor = "rgba(40,40,40,0.5)";
    }
    chosenKey = keyName;
    keyfield.textContent = keyName.replace("kp", "") + ":";
    document.getElementById("inputmod").focus();
    document.getElementById("inputmod").select();
}

//Deletes a key definition from the keydata, since we don't need "unmodifieds" - it's unnecessary information.
function deleteKey(key) {
    var keyCard = document.getElementById("keycard-" + key.displayName);
    keyCard.parentElement.removeChild(keyCard);
    var indexToremove = chosenProfile.getKeyIndex(key);
    chosenProfile.keyData.splice(indexToremove, 1);
    document.getElementById("ainput").textContent = JSON.stringify(parsePostdata(), null, 4);
}

// A function for submitting a change to the key.
function submitMod() {
    if (chosenKey !== "") {
        if (chosenProfile.getKeybyName(chosenKey) === undefined) {
            chosenProfile.keyData[chosenProfile.keyData.length] = new Key(chosenKey, getRealname(chosenKey), getRealname(chosenKey));
            addKeycard(chosenKey, getRealname(chosenKey), chosenProfile.keyData[chosenProfile.keyData.length - 1]);
            modifyKey(chosenKey);
        }
        var mapping = document.getElementById("inputmod").value;
        var chosenKeylocal = chosenProfile.getKeybyName(chosenKey);
        var button = document.getElementById("button-" + chosenKey);
        if(mapping.includes("Profiles(") || mapping.includes("Mode(") || mapping.includes("profiles(") ){
            chosenKeylocal.profiles = eval(mapping);
        } else {
            delete chosenKeylocal.profiles;
            delete chosenKeylocal.toggle;
            chosenKeylocal.mappedEvdevName = parseMapping(mapping, chosenKeylocal);
            chosenKeylocal.mappedEvdevID = parseEvdevName(chosenKeylocal.mappedEvdevName);
            document.getElementById("keycard-" + chosenKey + "-text").textContent = chosenKeylocal.displayName + " - " +  chosenKeylocal.mappedEvdevName.replace(/KEY_/g,"").toLowerCase();
        }
        if(chosenKeylocal.profiles !== undefined){
            delete chosenKeylocal.mappedEvdevName;
            delete chosenKeylocal.mappedEvdevID;
        //    document.getElementById("keycard-" + chosenKey + "-text").textContent = chosenKeylocal.displayName + " - " + "Profiles: " + chosenKeylocal.profiles;
                if (chosenProfile.getKeybyName(chosenKey).toggle === true) {
                document.getElementById("keycard-" + chosenKey + "-text").textContent = chosenKeylocal.displayName + " - " + "Toggle profile: " + getProfilebyID(chosenProfile.getKeybyName(chosenKey).profiles[0]).profileName;                    
                } else {
                document.getElementById("keycard-" + chosenKey + "-text").textContent = chosenKeylocal.displayName + " - " + "Switch profile: " + getProfilebyID(chosenProfile.getKeybyName(chosenKey).profiles[0]).profileName;                    
                }
        }
        if (chosenKeylocal.EvdevID == chosenKeylocal.mappedEvdevID) {
            deleteKey(chosenKeylocal);
            button.textContent = chosenKeylocal.displayName;
        }
        if (chosenLayout.realNames === false) {
            button.textContent = chosenKeylocal.mappedEvdevName.replace(/KEY_/g, "").toLowerCase();
        }
        document.getElementById("ainput").textContent = JSON.stringify(parsePostdata(), null, 4);
    postKeys(parsePostdata(),"/update-profile");
    }
}

function getProfilebyID(profileID) {
    // Returns a profile, searched by ID.
    for (var i = 0; i < kbProfiles.length; i++) {
        if (profileID == kbProfiles[i].profileID) {
            return kbProfiles[i];
        }
    }
    return false;
}

function getProfilebyName(profileName) {
    // Returns a profile, searched by ID.
    for (var i = 0; i < kbProfiles.length; i++) {
        if (profileName == kbProfiles[i].profileName) {
            return kbProfiles[i];
        }
    }
    return false;
}

//Parses the string sent from submit, splitting it at designated char and then searching for the 'real names' or 'evdev names' of the mapped keystrokes, returning the resulting string of all those names.
function parseMapping(mapping, chosenKeylocal){
    var realnameString = "";
    if (mapping.includes("|") || mapping.includes("write(") || mapping.includes("repeat(") || mapping.includes("w(")) {
        var mappingArray = mapping.split("|");
        for (var i = 0; i < mappingArray.length; i++) {
            if(mappingArray[i].includes("write(") || mappingArray[i].includes("repeat(") || mappingArray[i].includes("w(")) mappingArray[i] = eval(mappingArray[i]);
            if (realnameString !== "" && realnameString.slice(-1)!=="|") {
                realnameString = realnameString + ":" + parseMapping(mappingArray[i]);
            } else {
                realnameString = realnameString + parseMapping(mappingArray[i]);
            }
            if(i !== mappingArray.length-1){realnameString = realnameString+"|";}
        }
    } else {
    if(mapping.includes(":")){var mappingArray = mapping.split(":")} else {var mappingArray = []; mappingArray[0] = mapping;};
    for(var i = 0; i<mappingArray.length; i++){
    if(getRealname(mappingArray[i])===undefined && mappingArray[i].includes("delay(") == false  && mappingArray[i].includes("$")==false || mappingArray[i]==="" && mappingArray[i].includes("delay(") == false && mappingArray[i].includes("$")==false){
        createNotification("Invalid input with " + mappingArray[i] + "!",true);
        return chosenKeylocal.mappedEvdevName;
    } else {
        if(realnameString!==""){
        if(mappingArray[i].includes("delay(") == false && mappingArray[i].includes("$")==false){
        realnameString = realnameString + ":" + getRealname(mappingArray[i]);
        } else {
            realnameString = realnameString;
            createNotification("Don't use delay with ':'!",true);
            }
        } else {
        if(mappingArray[i].includes("delay(") == false && mappingArray[i].includes("$")==false){
            realnameString = getRealname(mappingArray[i]);
        } else if(mappingArray[i].includes("$")==true && !isNaN(mappingArray[i].substring(1, mappingArray[i].length))) {
            realnameString = mappingArray[i];
        } else if(mappingArray[i].includes("$")==true && isNaN(mappingArray[i].substring(1, mappingArray[i].length))) {
            createNotification("Invalid input after $!",true);
            return chosenKeylocal.mappedEvdevName;
        } else {
            realnameString = eval(mappingArray[i]);
        }
        }
    }
    }
}
    return realnameString;
}

//Searches the layout profile for the keys, in case of layout issues.
function getRealname(input) {
    var evdevIDs = getAllEvdevIDs();
    for (var i = 0; i < chosenLayout.layoutArray.length; i++) {
        for (var j = 0; j < chosenLayout.layoutArray[i].length; j++) {
            if (input.toUpperCase() == chosenLayout.layoutArray[i][j][0].toUpperCase() && typeof chosenLayout.layoutArray[i][j][2] !== 'undefined') {
                return "KEY_" + chosenLayout.layoutArray[i][j][2].toUpperCase()
            } else if (input.toUpperCase() == chosenLayout.layoutArray[i][j][0].toUpperCase()) {
                return "KEY_" + chosenLayout.layoutArray[i][j][0].toUpperCase()
            };
        }
    }
    for (var i = 0; i < evdevIDs.length; i++) {
        if (evdevIDs[i][0] == input) {
            return evdevIDs[i][0];
        }
    }
}

//Parses the evdev name, returning any and all evdev ids.
function parseEvdevName(input) {
    var realidString = "";
    if(input === undefined) return;
    if (input.includes("|")) {
        var mappingArray = input.split("|");
        for (var i = 0; i < mappingArray.length; i++) {
            if (realidString !== "" && realidString.slice(-1)!=="|") {
                realidString = realidString + ":" + parseEvdevName(mappingArray[i]);
            } else {
                realidString = realidString + parseEvdevName(mappingArray[i]);
            }
            if(i !== mappingArray.length-1){realidString = realidString+"|";}
        }
    } else {
        if (input.includes(":")) {
            var mappingArray = input.split(":")
        } else {
            var mappingArray = [];
            mappingArray[0] = input;
        };
        for (var i = 0; i < mappingArray.length; i++) {
            if (realidString !== "") {
                if(mappingArray[i].includes("$") == false){
                realidString = realidString + ":" + getEvdevID(mappingArray[i]);
                } else {
                realidString = realidString + ":" + mappingArray[i];
                }
            } else {
                if(mappingArray[i].includes("$") == false){
                    realidString = getEvdevID(mappingArray[i]);
                    } else {
                    realidString = mappingArray[i];
                    }
            }
        }
    }
    return realidString;
}

//Changes the format of the data, so that it is fitting for the backend
function parsePostdata(){
    var postableProfiles = [];
    for(var i = 0; i<kbProfiles.length; i++){
    postableProfiles[i] = {};
    postableProfiles[i].profileName = kbProfiles[i].profileName;
    postableProfiles[i].profileID = kbProfiles[i].profileID;
    postableProfiles[i].keyData = {};
    for(var j = 0; j<kbProfiles[i].keyData.length; j++){
    postableProfiles[i].keyData[kbProfiles[i].keyData[j].EvdevID] = {};
    if(kbProfiles[i].keyData[j].profiles !== undefined){
        postableProfiles[i].keyData[kbProfiles[i].keyData[j].EvdevID].profiles = kbProfiles[i].keyData[j].profiles;
        postableProfiles[i].keyData[kbProfiles[i].keyData[j].EvdevID].toggle = kbProfiles[i].keyData[j].toggle;
    } else {
        postableProfiles[i].keyData[kbProfiles[i].keyData[j].EvdevID].mappedEvdevID = String(kbProfiles[i].keyData[j].mappedEvdevID);
        postableProfiles[i].keyData[kbProfiles[i].keyData[j].EvdevID].mappedEvdevName = kbProfiles[i].keyData[j].mappedEvdevName;
    }
    postableProfiles[i].keyData[kbProfiles[i].keyData[j].EvdevID].displayName = kbProfiles[i].keyData[j].displayName;
    postableProfiles[i].keyData[kbProfiles[i].keyData[j].EvdevID].evdevName = kbProfiles[i].keyData[j].evdevName;
    }
    }
    return postableProfiles;
}

//Posts the JSON to server. PARAMS: Profile, url to post
function postKeys(data, urli) {
    var postRequest = new XMLHttpRequest();
    postRequest.onreadystatechange = function () {
        if(postRequest.readyState === XMLHttpRequest.DONE && postRequest.status === 200) {
          createNotification("Successfully posted the keys!");
        }
      };

      postRequest.onerror = function onError(e) {
        createNotification("Error " + e.target.status + " occurred. Failed to post the keys. Check web server status.",true);
    }
    postRequest.open("POST", urli, true);
    postRequest.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
    postRequest.send(JSON.stringify(data));
    postRequest.onloadend = function() {};
}

//Prototype to load a profile
function loadProfiles() {
    var profilesJsonInitial = getJson("/json.api");
   // var profilesJsonInitial = '[{}]'
   // profilesJson[0] = new Profile("Profile-1", 1, []);
   try {
    profilesJson = JSON.parse(profilesJsonInitial);
    for(var i = 0; i<profilesJson.length; i++){
        kbProfiles[i] = new Profile(profilesJson[i].profileName, profilesJson[i].profileID, []);
        for (var j = 0; j < Object.keys(profilesJson[i].keyData).length; j++) {
            kbProfiles[i].keyData[j] = new Key(profilesJson[i].keyData[Object.keys(profilesJson[i].keyData)[j]].displayName, profilesJson[i].keyData[Object.keys(profilesJson[i].keyData)[j]].mappedEvdevName, profilesJson[i].keyData[Object.keys(profilesJson[i].keyData)[j]].evdevName);
            if(profilesJson[i].keyData[Object.keys(profilesJson[i].keyData)[j]].toggle !== undefined){
            delete kbProfiles[i].keyData[j].mappedEvdevID;
            delete kbProfiles[i].keyData[j].mappeEvdevName;
            kbProfiles[i].keyData[j].toggle = profilesJson[i].keyData[Object.keys(profilesJson[i].keyData)[j]].toggle;
            kbProfiles[i].keyData[j].profiles =  profilesJson[i].keyData[Object.keys(profilesJson[i].keyData)[j]].profiles;
            }
        }
    }
    chosenProfile = kbProfiles[0];
} catch(err) {
if(profilesJsonInitial !== '[{}]') createNotification(err + "! Creating empty data.", true);
kbProfiles[0] = new Profile("Profile-1", 1, []);
chosenProfile = kbProfiles[0];
}
}
//A function to create both error and success messages. Takes a string and boolean, if boolean is true, message is for an error.
function createNotification(string, error){
    var newNotification = document.createElement("div");
    newNotification.className = "success notification";
    newNotification.textContent = string;
    newNotification.setAttribute("top", 0.3*window.innerHeight);
    newNotification.style.top = newNotification.getAttribute("top") + "px";
    if (error === true) newNotification.className = "error notification";
    var wrapper = document.getElementById("bigwrap");
    wrapper.appendChild(newNotification);
    var notifications = document.getElementsByClassName("notification");
    for(var i = 0; i<notifications.length; i++){
        if(notifications[i] !== newNotification){
        var difference = parseInt(newNotification.clientHeight) + 5;
        notifications[i].setAttribute("top",parseInt(notifications[i].getAttribute("top"))+difference);
        notifications[i].style.top = notifications[i].getAttribute("top")+"px";
        }
    }
    var time = 0;
    var fade = setInterval(fadeNotification, 20);
    function fadeNotification() {
      if (time > 99) {
        newNotification.style.opacity = 0;
        setTimeout(function(){wrapper.removeChild(newNotification);},1000);
        clearInterval(fade);
      } else {
        time++;
      }
    }
}

//Gets profile from the url
function getJson(url) {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        xmlhttp = new XMLHttpRequest();
    } else {
        xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange = function() {
        if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {
        //    createNotification("Success!");
            return xmlhttp.responseText;
        } else {
        //    createNotification("Failed to load json: check server status.",true);
        }
    }
    xmlhttp.onerror = function onError(e) {
        createNotification("Error " + e.target.status + " occurred.",true);
    }
    xmlhttp.open("GET", url, false);
    xmlhttp.send();
    return xmlhttp.onreadystatechange();
}

//Function to ease input for user. Takes a string and returns a list of keystrokes.
function write(string){
    try {
    var newString = "";
    for(var i = 0; i<string.length; i++){
    newString = newString + string.charAt(i);
    if(i<string.length-1) newString = newString + "|";
    }
    return newString;
} catch(err) {
    createNotification(err,true);
    return "";
}
}

function w(string){
    return write(string);
}

//Function to repeat a string or key.
function repeat(string,count){
    string = string.replace(/>/g,'|');
    if(count>50){
        count=50;
        createNotification("Unreasonably high amount of repeats! Limiting to fifty.",true);
    }
    var oneCount = string;
    for(var i = 1; i<count; i++){
    string  = string + "|" + oneCount;
    }
    return string;
}

//Used for defining a function that either browses profiles or toggles them.
function Profiles(profiles,toggle){
    var profilesArray = [];
    var profileIDArray = [];
    profiles = profiles.toString();
    if(profiles.includes(",") && toggle !== true){
    profilesArray = profiles.split(',');
    } else {
    profilesArray[0] = profiles;
    }
    var newIndex = 0;
    for(var i = 0; i<profilesArray.length; i++){
        if(getProfilebyID(profilesArray[i]) !== false){
            profileIDArray[newIndex] = parseInt(profilesArray[i]);
            newIndex++;
        } else if(getProfilebyName(profilesArray[i]) !== false){
            profileIDArray[newIndex] = getProfilebyName(profilesArray[i]).profileID;
            newIndex++;
        } else {
            createNotification("Profile " + profilesArray[i] + " not found!",true);
            return undefined;
        }
    }
    if(toggle !== undefined){
        chosenProfile.getKeybyName(chosenKey).toggle = toggle;
    } else {
        chosenProfile.getKeybyName(chosenKey).toggle = false;
    }
    return profileIDArray;
}

function profiles(profiles,toggle){
    return Profiles(profiles,toggle);
}

//Can be used to make a button to work as shift or capslock.
function Mode(profile,toggle){
    profile = profile.toString();
    if(profile.includes(",")){
        profile = profile.split(',');
        profile = profile[0];
    }
   return Profiles(profile,toggle);
}

//Returns a formatted delay.
function delay(amount){
    return "$" + amount;
}
