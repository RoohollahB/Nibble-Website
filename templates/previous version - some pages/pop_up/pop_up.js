
window.addEventListener('load', function(){
     
    var elements = document.querySelectorAll("body *");
    var fontHash = {};
 
    for(var e=0;e<elements.length;e++){
        var elementStyles = window.getComputedStyle(elements[e],null);
        var df = elementStyles['font-family'];
 
        df = df.split('-').join(' ')
            .split('+').join(' ')
            .split(' ').join('')
            .toLowerCase();
 
        for(var gf = 0; gf<gfl.length; gf++){
            if(df.indexOf(gfl[gf].split(' ').join('').toLowerCase())>-1){
		        var fontName = gfl[gf];
                if(!fontHash[fontName]) _agfh(gfl[gf]+':400,700,800');
                fontHash[fontName] = 1;
            }
        }
    }
 
    function _agfh(n){
       var gfli = "<link rel='stylesheet' href='https://fonts.googleapis.com/css?family="+n+"'>";
	   document.head.innerHTML = document.head.innerHTML + gfli;
    }

    function closeWindow() {
        window.close();
    }

    function changeEmail() {
        var newEmail = prompt('Enter new email:');
        
        if (newEmail) {
            document.getElementById('emailDisplay').textContent = newEmail;
        }
    }
    
    
},false);