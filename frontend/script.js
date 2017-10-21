// Class for profiles.
class Profile {
    constructor(profileName, profileID, keyData) {
        this.profileName = profileName;
        this.profileID = profileID;
        this.keyData = keyData;
    }

// Gets a key from the profile's keydata with a provided key ID.
    getKeybyID(keyID){
        for(var i = 0; i<this.keyData.length; i++){
            if(keyID == this.keyData[i].keyID){
                return this.keyData[i];
            } 
        }
        console.log("No key found with ID of " + keyID);
        return;
    }
}

// Class for keys.
class Key {
    constructor(keyID, keyName, mappedID, mappedName) {
        this.keyID = keyID;
        this.keyName = keyName;
        this.mappedID = mappedID;
        this.mappedName = mappedName;
    }
}

// Some test values, as well as calls for initiating the keyboard and keycards.
var finLayout = [
    [["Esc",1],["",1],["F1",1],["F2",1],["F3",1],["F4",1],["",0.25],["F5",1],["F6",1],["F7",1],["F8",1],["",0.25],["F9",1],["F10",1],["F11",1],["F12",1],["",1],["Print Screen",1],["Scroll Lock",1],["Pause",1],["",1.5],["",1],["",1],["",1],["",1]],
    [["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],["",1],[""]],
    [["§",1],["1",1],["2",1],["3",1],["4",1],["5",1],["6",1],["7",1],["8",1],["9",1],["0",1],["+",1],["´",1],["<=",2],["",1],["Insert",1],["Home",1],["Page Up",1],["",1],["Num Lock",1],["/",1],["*",1],["num-",1],[""]],
    [["Tab",1.5],["q",1],["w",1],["e",1],["r",1],["t",1],["y",1],["u",1],["i",1],["o",1],["p",1],["å",1],["^",1],["Enter",1.5],["",1],["Del",1],["End",1],["Page Down",1],["",1],["num7",1],["num8",1],["num9",1],["num+",1],["",1],[""]],
    [["Caps",1.75],["a",1],["s",1],["d",1],["f",1],["g",1],["h",1],["j",1],["k",1],["l",1],["ö",1],["ä",1],["'",1],["Enter",1.25],["",1],["",1],["",1],["",1],["",1],["num4",1],["num5",1],["num6",1],["num+",1],[""]],
    [["Shift",1.25],["<",1],["z",1],["x",1],["c",1],["v",1],["b",1],["n",1],["m",1],[",",1],[".",1],["-",1],["RShift",2.9],["",1],["",1],["Up",1],["",1],["",1],["num1",1],["num2",1],["num3",1],["numEnter",1],["",1],[""]],
    [["Ctrl",1.5],["Win/Function",1.25],["Alt",1.25],["Space",7],["RAlt",1.25],["win/Function",1.25],["Menu",1.25],["Ctrl",1.25],["",1],["Left",1],["Down",1],["Right",1],["",1],["num0",2.2],["numDel",1],["numEnter",1],["",1],["",1]
    ]];
var kbProfiles = [];
kbProfiles[0] = new Profile("testi", 0, ["", ""]);
var chosenProfile = kbProfiles[0];
var chosenKey = "";
initiateKeyboard();
addProfilecards();
changeProfile(0,document.getElementById("profile-" + kbProfiles[0].profileID));


// Builds the visualized keyboard based on an array. Array has rows of keys, with each key containing two values - the displayed characters and the width in relation to a "normal" key.
function initiateKeyboard() {
    var k = 0;
    for (var i = 0; i < finLayout.length; i++) {
            var rowwrapper = document.createElement("div");
            rowwrapper.className = "rowwrapper";
            rowwrapper.id = "row-" + i;
        for (var j = 0; j < finLayout[i].length; j++) {
            var buttonwrapper = document.createElement("div");
            buttonwrapper.className = "buttonwrapper";
            buttonwrapper.id = "wrapper-" + finLayout[i][j][0];
            var keybutton = document.createElement("button");
            keybutton.className = "keybutton";
            keybutton.id = "button-" + finLayout[i][j][0];
            if (finLayout[i][j][0] != "") {
                chosenProfile.keyData[k] = new Key(k, finLayout[i][j][0], k, finLayout[i][j][0]);
                keybutton.setAttribute("keyID",chosenProfile.keyData[k].keyID);
                k++;
            }
            //Adds listener to the buttons on the keyboard.
            keybutton.addEventListener("click", function() {
                modifyKey(this.getAttribute("keyID"));
            }, false);
            if (finLayout[i][j][0].includes("num")) {
                keybutton.textContent = finLayout[i][j][0].replace("num", "");
            } else {
                keybutton.textContent = finLayout[i][j][0];
            }
            if (keybutton.textContent == "") keybutton.style.display = "none";
            var newwidth = finLayout[i][j][1] * parseInt(30);
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
                submitchange.addEventListener("click", function() {
                submitMod();
    }, false);
}

// Deletes the old key definition cards, and then rebuilds new ones. Used when changing profiles.
function addKeycards() {
    var defWrap = document.getElementById("keydefs");
    defWrap.innerHTML = "";
    for (var i = 0; i < chosenProfile.keyData.length; i++) {
        addKeycard(chosenProfile.keyData[i].keyName, chosenProfile.keyData[i].keyID, chosenProfile.keyData[i].mappedName);
    }
}

// Adds new profile cards, deleting any that had been there before.
function addProfilecards(){
    var profWrap = document.getElementById("profcards");
    profWrap.innerHTML = "";
    for(var i = 0; i<kbProfiles.length; i++){
        addProfilecard(kbProfiles[i]);
    }
}

// Adds a new profile and a card for it.
function addProfile(name,keydata){
    var newIndex = kbProfiles.length;
    kbProfiles[newIndex] = new Profile(name,newIndex,keydata);
    addProfilecard(kbProfiles[newIndex]);
}

// Adds a new key definition card.
function addKeycard(keyName, keyID, mappedName){
    var defWrap = document.getElementById("keydefs");
    var keyCard = document.createElement("div");
    keyCard.className = "card";
    keyCard.id = "keycard-" + keyName;
    keyCard.setAttribute("keyID",keyID);
    keyCard.textContent = keyName + " - " + mappedName;
    // Listener for clicks on the card: functions the same as clicking a button on the visualized keyboard, selecting the key.
    keyCard.addEventListener("click", function() {
    modifyKey(this.getAttribute("keyID"));
}, false);
    defWrap.appendChild(keyCard);
}

// Adds a profile card.
function addProfilecard(profile){
    var profWrap = document.getElementById("profcards");
    var profileCard = document.createElement("div");
    profileCard.className = "card";
    profileCard.id = "profile-" + profile.profileID;
    profileCard.setAttribute("profileID", profile.profileID);
    profileCard.textContent = profile.profileName;
    profileCard.addEventListener("click", function() {
    changeProfile(this.getAttribute("profileID"),this);
}, false);
    profWrap.appendChild(profileCard);
}

// Creates a fresh key data.
function createEmptyKeyData(){
    var keyData = [];
    var k = 0;
    for(var i = 0; i<finLayout.length; i++){
        for(var j = 0; j<finLayout[i].length; j++){
            if (finLayout[i][j][0] != "") {
                keyData[k] = new Key(k, finLayout[i][j][0], k, finLayout[i][j][0]);
                k++;
            }
        }
    }
    return keyData;
}

// Changes the chosen profile, resetting the background color of the old chosen profile.
function changeProfile(newIndex, profileCard){
    var oldProfilecard = document.getElementById("profile-" + chosenProfile.profileID);
    oldProfilecard.style.backgroundColor = "";
    chosenProfile = kbProfiles[newIndex];
    profileCard.style.backgroundColor = "green";
    addKeycards();
}

// When a key is chosen on the visualized keyboard, this is fired. It updates the chosen key and highlights the keycard, as well as removes any older highlights.
function modifyKey(keyid) {
    if (keyid != undefined) {
        var keyField = document.getElementById("keyfield");
        var keyName = chosenProfile.getKeybyID(keyid).keyName;
        keyfield.textContent = keyName.replace("num", "") + ":";
        if (document.getElementById("keycard-" + chosenKey.keyName) != null) document.getElementById("keycard-" + chosenKey.keyName).style.backgroundColor = "";
        var keyCard = document.getElementById("keycard-" + keyName);
        keyCard.style.backgroundColor = "green";
    }
    chosenKey = chosenProfile.getKeybyID(keyid);
}

// A function for submitting a change to the key.
function submitMod() {
    var chosenKeyName = chosenKey.keyName;
    var keyCard = document.getElementById("keycard-" + chosenKeyName);
    var mappedName = document.getElementById("inputmod").value;
    chosenProfile.keyData[keyCard.getAttribute("keyID")].mappedName = mappedName;
    document.getElementById("keycard-" + chosenKeyName).textContent = chosenKey.keyName + "-" + chosenKey.mappedName;
}