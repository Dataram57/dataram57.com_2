
const ParseJSON = (e) => {
    try{
        return JSON.parse(e);
    }
    catch{
        return undefined;
    }
}

//================================================================
//#region Dark Mode Button

/*
const InitDarkMode = () => {
    //load from memory
    let i = ParseJSON(window.localStorage.getItem("dark_mode"));
    if(i === undefined)
        window.localStorage.setItem('dark_mode', true);
    else if(i == false)
        document.documentElement.classList.toggle("dark-mode");
};
*/


const InitDarkModeButton = () => {
    //setup button
    const element = document.getElementById("dark_mode_button");
    if(element){
        element.href = "javascript:void(0)";
        element.onclick = onDarkModeButtonClicked;
    }
};

const onDarkModeButtonClicked = (e) => {
    //change memory
    window.localStorage.setItem('dark_mode', !document.documentElement.classList.contains("dark-mode"));
    
    //change class
    document.documentElement.classList.toggle("dark-mode");
};

//#endregion

//================================================================
//#region Startup

//InitDarkMode();
window.onload = InitDarkModeButton;

//#endregion
