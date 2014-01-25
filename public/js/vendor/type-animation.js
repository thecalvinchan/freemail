//FUNCTION: animateType
//PARAMETERS: dom - DOM element, lines - array of lines to render

var animateType = function(dom,lines) {
    console.log(dom,lines);
    //Tokenizing chars
    var charArray = [];
    for (var j=0;j<lines.length;j++) {
        charArray.push("<p>");
        for (var k=0;k<lines[j].length;k++) {
            charArray.push(lines[j][k]);
        }
        charArray.push("</p>");
    }
    //Rendering text
    renderText(dom,charArray);        
};

function renderText(dom,charArray) {
        var _this = {};
        _this.dom = dom;
        _this.charArray = charArray;
        setTimeout((function() {
            dom.innerHTML += charArray.shift();
            if(charArray.length > 0) {
                renderText(dom,charArray);
            }
        }).bind(_this), 50);
}


