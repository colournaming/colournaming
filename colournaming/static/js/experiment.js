(()=>{var o=JSON.parse(localStorage.getItem("results")),H=()=>{let e=document.getElementById("mturk-code");navigator.clipboard.writeText(e.innerText)};window.copyMturkCodeToClipboard=H;var n=e=>{o=Object.assign({},o,e),localStorage.setItem("results",JSON.stringify(o))},f=document.getElementById("levels");window.location.href.endsWith("observer_information.html")&&navigator.geolocation&&navigator.geolocation.getCurrentPosition(function(e){n({location:String(e.coords.latitude+","+e.coords.longitude)})});var g=(e,d)=>{let c=new FormData;c.append("csrf_token",document.getElementById("csrf_token").value),Object.keys(e).forEach(t=>{c.append(t,e[t])}),fetch(window.location,{body:c,credentials:"same-origin",method:"POST"}).then(t=>{if(!t.ok)throw new Error(`HTTP error ${res.status}`);return console.log(t),t.redirected?(console.log("redirecting"),window.location=t.url):typeof d=="string"&&(console.log("setting window.location to location"),window.location=d),t}).catch(t=>console.error("Error:",t))};f!==null&&(n({greyscaleRampSteps:void 0}),f.addEventListener("change",()=>{let e=f.value;e!=="-"?(n({greyscaleRampSteps:parseInt(e,10)}),g({levels:e,screen_colour_depth:screen.colorDepth,screen_height:screen.height,screen_width:screen.width},"name_colour.html")):n({greyscaleRampSteps:void 0})}));var y=document.getElementById("colour-circle"),p=document.getElementById("colour-id"),r=document.getElementById("colour-name"),N=document.getElementById("colour-name-form"),j=document.getElementById("colour-number"),P=document.getElementById("colour-vision-test-page"),q=document.getElementById("next-colour"),v=document.getElementById("response-time"),h=document.getElementById("start-time");if(y!==null&&p!==null&&r!==null&&N!==null&&j!==null&&P!==null&&q!==null&&v!==null&&h!==null){n({colours:void 0});let e=()=>{fetch(COLOUR_NAME_TARGET_URL).then(t=>t.json()).then(({b:t,g:i,id:a,r:s})=>{y.style.backgroundColor=`rgb(${s}, ${i}, ${t})`,p.value=a,h.value=performance.now()})},d=()=>{let t={name:r.value,value:y.style.backgroundColor},i=o.colours?[...o.colours,t]:[t];n({colours:i})};e(),r.addEventListener("input",()=>{v.value===""&&(v.value=performance.now()-parseFloat(h.value))}),N.addEventListener("submit",t=>{t.preventDefault(),d(),g({name:r.value,response_time:parseFloat(v.value),target_id:p.value}),e(),r.value="",j.textContent=`#${o.colours?o.colours.length+1:0}`,v.value="",r.focus()}),P.addEventListener("click",t=>{t.preventDefault(),r.value!==""?(d(),g({name:r.value,response_time:performance.now()-parseFloat(h.value),target_id:p.value},"colour_vision.html")):window.location="colour_vision.html"});let c={height:window.innerHeight,width:window.innerWidth};window.addEventListener("resize",()=>{let t=window.innerHeight,i=document.scrollingElement.scrollTop,a=window.innerWidth;if(r===document.activeElement&&t<c.height&&a===c.width){let{height:s,top:u}=r.getBoundingClientRect(),m=u+i-t+s+10;document.scrollingElement.scrollTop=m;let l=0,F=()=>{document.scrollingElement.scrollTop!==m&&(document.scrollingElement.scrollTop=m),l+=1,l<20&&requestAnimationFrame(F)};requestAnimationFrame(F)}c={height:t,width:a}})}var E=document.getElementById("appearance");E!==null&&(n({appearance:void 0}),E.addEventListener("change",()=>{let e=E.value;e!=="-"?(n({appearance:e}),g({square_disappeared:e},"observer_information.html")):n({appearance:void 0})}));var _=document.getElementById("age"),w=document.getElementById("gender"),C=document.getElementById("gender_other"),I=document.getElementById("colour_experience"),B=document.getElementById("language_experience"),L=document.getElementById("education_level"),T=document.getElementById("country_raised"),k=document.getElementById("country_resident"),b=document.getElementById("ambient_light"),x=document.getElementById("screen_temperature"),S=document.getElementById("display_device"),O=document.getElementById("screen_light"),D=document.getElementById("screen_distance"),R=document.getElementById("thank-you-page");_!==null&&D!==null&&L!==null&&O!==null&&I!==null&&w!==null&&C!==null&&T!==null&&B!==null&&b!==null&&x!==null&&k!==null&&S!==null&&R!==null&&(n({age:-1,distance:-1,educationalLevel:"",environment:"",experience:"",gender:"",genderOther:"",homeCountry:"",languageSkills:"",lightConditions:"",screenTemperature:"",residentCountry:"",displayDevice:""}),_.addEventListener("change",()=>{let e=_.value;n(e!=="-"?{age:parseInt(e,10)}:{age:void 0})}),D.addEventListener("change",()=>{let e=D.value;n(e!=="-"?{distance:e}:{distance:void 0})}),L.addEventListener("change",()=>{let e=L.value;n(e!=="-"?{educationalLevel:e}:{educationalLevel:void 0})}),O.addEventListener("change",()=>{let e=O.value;n(e!=="-"?{environment:e}:{environment:void 0})}),x.addEventListener("change",()=>{let e=x.value;n(e!=="-"?{screenTemperature:e}:{screenTemperature:void 0})}),I.addEventListener("change",()=>{let e=I.value;n(e!=="-"?{experience:e}:{experience:void 0})}),w.addEventListener("change",()=>{let e=w.value;n(e!=="-"?{gender:e}:{gender:void 0}),e=="other"?$("#specify-gender").show():$("#specify-gender").hide()}),C.addEventListener("change",()=>{let e=C.value;n(e!==""?{genderOther:e}:{genderOther:void 0})}),T.addEventListener("change",()=>{let e=T.value;n(e!=="-"?{homeCountry:e}:{homeCountry:void 0})}),B.addEventListener("change",()=>{let e=B.value;n(e!=="-"?{languageSkills:e}:{languageSkills:void 0})}),b.addEventListener("change",()=>{let e=b.value;n(e!=="-"?{lightConditions:e}:{lightConditions:void 0})}),k.addEventListener("change",()=>{let e=k.value;n(e!=="-"?{residentCountry:e}:{residentCountry:void 0})}),S.addEventListener("change",()=>{let e=S.value;n(e!=="-"?{displayDevice:e}:{displayDevice:void 0})}),R.addEventListener("click",e=>{e.preventDefault(),g({age:o.age,ambient_light:o.lightConditions,colour_experience:o.experience,country_raised:o.homeCountry,country_resident:o.residentCountry,education_level:o.educationalLevel,gender:o.gender,gender_other:o.genderOther,language_experience:o.languageSkills,screen_distance:o.distance,screen_light:o.environment,screen_temperature:o.screenTemperature,display_device:o.displayDevice,location:o.location},R.href)}));var M=document.getElementById("thank-you-text"),A=document.getElementById("results");if(M!==null&&A!==null){let{colours:e}=o;e&&Promise.all(Object.keys(e).map(d=>{let{name:c,value:t}=e[d],i=document.createElement("div"),a=document.createElement("li"),s=document.createElement("span"),u=document.createElement("span");i.style.backgroundColor=t,s.className="white",s.textContent=c;let m=t.match(/rgb\(([0-9]+),\s([0-9]+),\s([0-9]+)\)/).slice(1).map(l=>parseInt(l,10)).map(l=>l.toString(16)).join("");return a.appendChild(i),a.appendChild(s),a.appendChild(u),A.appendChild(a),fetch(`/namer/lang/default/name?colour=${m}`,{credentials:"same-origin"}).then(l=>l.json()).then(l=>{u.className="black",u.textContent=l.colours[0].name.replace("_"," ")})}))}})();
//# sourceMappingURL=experiment.js.map
