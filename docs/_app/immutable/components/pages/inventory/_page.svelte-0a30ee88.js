import{_ as st,S as Ft,i as Gt,s as Zt,k as F,a as K,l as G,m as H,c as J,h as x,n as T,b as te,G as I,B as Ae,a4 as Ke,O as xe,q as Re,r as Ne,p as Te,K as ne,Z as Ut,a5 as jt,d as Je,f as ee,t as oe,L as Wt,w as Le,x as Se,y as Ce,ag as zt,ah as Bt,z as $e,u as Vt,g as Qe,ai as Ht}from"../../../chunks/index-db041984.js";import{c as mn,W as En,T as Dn}from"../../../chunks/index-611c23b5.js";const _n="finalize",yn="consider";function ge(e,t,n){e.dispatchEvent(new CustomEvent(_n,{detail:{items:t,info:n}}))}function se(e,t,n){e.dispatchEvent(new CustomEvent(yn,{detail:{items:t,info:n}}))}const je="draggedEntered",ye="draggedLeft",We="draggedOverIndex",lt="draggedLeftDocument",Pe={LEFT_FOR_ANOTHER:"leftForAnother",OUTSIDE_OF_ANY:"outsideOfAny"};function vn(e,t,n){e.dispatchEvent(new CustomEvent(je,{detail:{indexObj:t,draggedEl:n}}))}function wn(e,t,n){e.dispatchEvent(new CustomEvent(ye,{detail:{draggedEl:t,type:Pe.LEFT_FOR_ANOTHER,theOtherDz:n}}))}function On(e,t){e.dispatchEvent(new CustomEvent(ye,{detail:{draggedEl:t,type:Pe.OUTSIDE_OF_ANY}}))}function Tn(e,t,n){e.dispatchEvent(new CustomEvent(We,{detail:{indexObj:t,draggedEl:n}}))}function bn(e){window.dispatchEvent(new CustomEvent(lt,{detail:{draggedEl:e}}))}const Z={DRAG_STARTED:"dragStarted",DRAGGED_ENTERED:je,DRAGGED_ENTERED_ANOTHER:"dragEnteredAnother",DRAGGED_OVER_INDEX:We,DRAGGED_LEFT:ye,DRAGGED_LEFT_ALL:"draggedLeftAll",DROPPED_INTO_ZONE:"droppedIntoZone",DROPPED_INTO_ANOTHER:"droppedIntoAnother",DROPPED_OUTSIDE_OF_ANY:"droppedOutsideOfAny",DRAG_STOPPED:"dragStopped"},j={POINTER:"pointer",KEYBOARD:"keyboard"},ze="isDndShadowItem",at="data-is-dnd-shadow-item",ct="id:dnd-shadow-placeholder-0000",In="dnd-action-dragged-el";let C="id",et=0;function Yt(){et++}function Xt(){if(et===0)throw new Error("Bug! trying to decrement when there are no dropzones");et--}const dt=typeof window>"u";function qt(e){let t;const n=e.getBoundingClientRect(),r=getComputedStyle(e),o=r.transform;if(o){let i,s,l,c;if(o.startsWith("matrix3d("))t=o.slice(9,-1).split(/, /),i=+t[0],s=+t[5],l=+t[12],c=+t[13];else if(o.startsWith("matrix("))t=o.slice(7,-1).split(/, /),i=+t[0],s=+t[3],l=+t[4],c=+t[5];else return n;const d=r.transformOrigin,u=n.x-l-(1-i)*parseFloat(d),f=n.y-c-(1-s)*parseFloat(d.slice(d.indexOf(" ")+1)),a=i?n.width/i:e.offsetWidth,p=s?n.height/s:e.offsetHeight;return{x:u,y:f,width:a,height:p,top:f,right:u+a,bottom:f+p,left:u}}else return n}function Kt(e){const t=qt(e);return{top:t.top+window.scrollY,bottom:t.bottom+window.scrollY,left:t.left+window.scrollX,right:t.right+window.scrollX}}function ut(e){const t=e.getBoundingClientRect();return{top:t.top+window.scrollY,bottom:t.bottom+window.scrollY,left:t.left+window.scrollX,right:t.right+window.scrollX}}function Jt(e){return{x:(e.left+e.right)/2,y:(e.top+e.bottom)/2}}function An(e,t){return Math.sqrt(Math.pow(e.x-t.x,2)+Math.pow(e.y-t.y,2))}function ft(e,t){return e.y<=t.bottom&&e.y>=t.top&&e.x>=t.left&&e.x<=t.right}function De(e){return Jt(ut(e))}function mt(e,t){const n=De(e),r=Kt(t);return ft(n,r)}function xn(e,t){const n=De(e),r=De(t);return An(n,r)}function Rn(e){const t=ut(e);return t.right<0||t.left>document.documentElement.scrollWidth||t.bottom<0||t.top>document.documentElement.scrollHeight}function Nn(e,t){const n=ut(t);return ft(e,n)?{top:e.y-n.top,bottom:n.bottom-e.y,left:e.x-n.left,right:Math.min(n.right,document.documentElement.clientWidth)-e.x}:null}let ue;function ht(){ue=new Map}ht();function Ln(e){ue.delete(e)}function Sn(e){const t=Array.from(e.children).findIndex(n=>n.getAttribute(at));if(t>=0)return ue.has(e)||ue.set(e,new Map),ue.get(e).set(t,Kt(e.children[t])),t}function Cn(e,t){if(!mt(e,t))return null;const n=t.children;if(n.length===0)return{index:0,isProximityBased:!0};const r=Sn(t);for(let s=0;s<n.length;s++)if(mt(e,n[s])){const l=ue.has(t)&&ue.get(t).get(s);return l&&!ft(De(e),l)?{index:r,isProximityBased:!1}:{index:s,isProximityBased:!1}}let o=Number.MAX_VALUE,i;for(let s=0;s<n.length;s++){const l=xn(e,n[s]);l<o&&(o=l,i=s)}return{index:i,isProximityBased:!0}}const Ee=25;function Qt(){let e;function t(){e={directionObj:void 0,stepPx:0}}t();function n(i){const{directionObj:s,stepPx:l}=e;s&&(i.scrollBy(s.x*l,s.y*l),window.requestAnimationFrame(()=>n(i)))}function r(i){return Ee-i}function o(i,s){if(!s)return!1;const l=Nn(i,s);if(l===null)return t(),!1;const c=!!e.directionObj;let[d,u]=[!1,!1];return s.scrollHeight>s.clientHeight&&(l.bottom<Ee?(d=!0,e.directionObj={x:0,y:1},e.stepPx=r(l.bottom)):l.top<Ee&&(d=!0,e.directionObj={x:0,y:-1},e.stepPx=r(l.top)),!c&&d)||s.scrollWidth>s.clientWidth&&(l.right<Ee?(u=!0,e.directionObj={x:1,y:0},e.stepPx=r(l.right)):l.left<Ee&&(u=!0,e.directionObj={x:-1,y:0},e.stepPx=r(l.left)),!c&&u)?(n(s),!0):(t(),!1)}return{scrollIfNeeded:o,resetScrolling:t}}function Xe(e){return JSON.stringify(e,null,2)}function Et(e){if(!e)throw new Error("cannot get depth of a falsy node");return en(e,0)}function en(e,t=0){return e.parentElement?en(e.parentElement,t+1):t-1}function $n(e,t){if(Object.keys(e).length!==Object.keys(t).length)return!1;for(const n in e)if(!{}.hasOwnProperty.call(t,n)||t[n]!==e[n])return!1;return!0}function Pn(e,t){if(e.length!==t.length)return!1;for(let n=0;n<e.length;n++)if(e[n]!==t[n])return!1;return!0}const kn=200,Dt=10,{scrollIfNeeded:Mn,resetScrolling:Fn}=Qt();let tt;function Gn(e,t,n=kn){let r,o,i=!1,s;const l=Array.from(t).sort((d,u)=>Et(u)-Et(d));function c(){const d=De(e),u=Mn(d,r);if(!u&&s&&Math.abs(s.x-d.x)<Dt&&Math.abs(s.y-d.y)<Dt){tt=window.setTimeout(c,n);return}if(Rn(e)){bn(e);return}s=d;let f=!1;for(const a of l){u&&Ln(r);const p=Cn(e,a);if(p===null)continue;const{index:w}=p;f=!0,a!==r?(r&&wn(r,e,a),vn(a,p,e),r=a):w!==o&&(Tn(a,p,e),o=w);break}!f&&i&&r?(On(r,e),r=void 0,o=void 0,i=!1):i=!0,tt=window.setTimeout(c,n)}c()}function Zn(){clearTimeout(tt),Fn(),ht()}const Un=300;let ke;function Me(e){const t=e.touches?e.touches[0]:e;ke={x:t.clientX,y:t.clientY}}const{scrollIfNeeded:jn,resetScrolling:Wn}=Qt();let tn;function nn(){ke&&jn(ke,document.documentElement)&&ht(),tn=window.setTimeout(nn,Un)}function zn(){window.addEventListener("mousemove",Me),window.addEventListener("touchmove",Me),nn()}function Bn(){window.removeEventListener("mousemove",Me),window.removeEventListener("touchmove",Me),ke=void 0,window.clearTimeout(tn),Wn()}function Vn(e){const t=e.cloneNode(!0),n=[],r=e.tagName==="SELECT",o=r?[e]:[...e.querySelectorAll("select")];for(const s of o)n.push(s.value);if(o.length<=0)return t;const i=r?[t]:[...t.querySelectorAll("select")];for(let s=0;s<i.length;s++){const l=i[s],c=n[s],d=l.querySelector(`option[value="${c}"`);d&&d.setAttribute("selected",!0)}return t}const Hn=.2;function ae(e){return`${e} ${Hn}s ease`}function Yn(e,t){const n=e.getBoundingClientRect(),r=Vn(e);rn(e,r),r.id=In,r.style.position="fixed";let o=n.top,i=n.left;if(r.style.top=`${o}px`,r.style.left=`${i}px`,t){const s=Jt(n);o-=s.y-t.y,i-=s.x-t.x,window.setTimeout(()=>{r.style.top=`${o}px`,r.style.left=`${i}px`},0)}return r.style.margin="0",r.style.boxSizing="border-box",r.style.height=`${n.height}px`,r.style.width=`${n.width}px`,r.style.transition=`${ae("top")}, ${ae("left")}, ${ae("background-color")}, ${ae("opacity")}, ${ae("color")} `,window.setTimeout(()=>r.style.transition+=`, ${ae("width")}, ${ae("height")}`,0),r.style.zIndex="9999",r.style.cursor="grabbing",r}function Xn(e){e.style.cursor="grab"}function qn(e,t,n,r){rn(t,e);const o=t.getBoundingClientRect(),i=e.getBoundingClientRect(),s=o.width-i.width,l=o.height-i.height;if(s||l){const c={left:(n-i.left)/i.width,top:(r-i.top)/i.height};e.style.height=`${o.height}px`,e.style.width=`${o.width}px`,e.style.left=`${parseFloat(e.style.left)-c.left*s}px`,e.style.top=`${parseFloat(e.style.top)-c.top*l}px`}}function rn(e,t){const n=window.getComputedStyle(e);Array.from(n).filter(r=>r.startsWith("background")||r.startsWith("padding")||r.startsWith("font")||r.startsWith("text")||r.startsWith("align")||r.startsWith("justify")||r.startsWith("display")||r.startsWith("flex")||r.startsWith("border")||r==="opacity"||r==="color"||r==="list-style-type").forEach(r=>t.style.setProperty(r,n.getPropertyValue(r),n.getPropertyPriority(r)))}function Kn(e,t){e.draggable=!1,e.ondragstart=()=>!1,t?(e.style.userSelect="",e.style.WebkitUserSelect="",e.style.cursor=""):(e.style.userSelect="none",e.style.WebkitUserSelect="none",e.style.cursor="grab")}function on(e){e.style.display="none",e.style.position="fixed",e.style.zIndex="-5"}function Jn(e){e.style.visibility="hidden",e.setAttribute(at,"true")}function Qn(e){e.style.visibility="",e.removeAttribute(at)}function be(e,t=()=>{},n=()=>[]){e.forEach(r=>{const o=t(r);Object.keys(o).forEach(i=>{r.style[i]=o[i]}),n(r).forEach(i=>r.classList.add(i))})}function Fe(e,t=()=>{},n=()=>[]){e.forEach(r=>{const o=t(r);Object.keys(o).forEach(i=>{r.style[i]=""}),n(r).forEach(i=>r.classList.contains(i)&&r.classList.remove(i))})}function er(e){const t=e.style.minHeight;e.style.minHeight=window.getComputedStyle(e).getPropertyValue("height");const n=e.style.minWidth;return e.style.minWidth=window.getComputedStyle(e).getPropertyValue("width"),function(){e.style.minHeight=t,e.style.minWidth=n}}const tr="--any--",nr=100,_t=3,yt={outline:"rgba(255, 255, 102, 0.7) solid 2px"};let Q,k,z,Be,R,Ve,pe,W,re,B,de=!1,gt=!1,pt,ve=!1,Ie=[];const X=new Map,A=new Map,qe=new WeakMap;function rr(e,t){X.has(t)||X.set(t,new Set),X.get(t).has(e)||(X.get(t).add(e),Yt())}function vt(e,t){X.get(t).delete(e),Xt(),X.get(t).size===0&&X.delete(t)}function ir(){zn();const e=X.get(Be);for(const n of e)n.addEventListener(je,sn),n.addEventListener(ye,ln),n.addEventListener(We,an);window.addEventListener(lt,me);const t=Math.max(nr,...Array.from(e.keys()).map(n=>A.get(n).dropAnimationDurationMs));Gn(k,e,t*1.07)}function or(){Bn();const e=X.get(Be);for(const t of e)t.removeEventListener(je,sn),t.removeEventListener(ye,ln),t.removeEventListener(We,an);window.removeEventListener(lt,me),Zn()}function sr(e){return e.findIndex(t=>t[C]===ct)}function He(e){return e.findIndex(t=>!!t[ze]&&t[C]!==ct)}function sn(e){let{items:t,dropFromOthersDisabled:n}=A.get(e.currentTarget);if(n&&e.currentTarget!==R)return;if(ve=!1,t=t.filter(s=>s[C]!==pe[C]),R!==e.currentTarget){const l=A.get(R).items.filter(c=>!c[ze]);se(R,l,{trigger:Z.DRAGGED_ENTERED_ANOTHER,id:z[C],source:j.POINTER})}else{const s=sr(t);s!==-1&&t.splice(s,1)}const{index:r,isProximityBased:o}=e.detail.indexObj,i=o&&r===e.currentTarget.children.length-1?r+1:r;W=e.currentTarget,t.splice(i,0,pe),se(e.currentTarget,t,{trigger:Z.DRAGGED_ENTERED,id:z[C],source:j.POINTER})}function ln(e){if(!de)return;const{items:t,dropFromOthersDisabled:n}=A.get(e.currentTarget);if(n&&e.currentTarget!==R&&e.currentTarget!==W)return;const r=He(t),o=t.splice(r,1)[0];W=void 0;const{type:i,theOtherDz:s}=e.detail;if(i===Pe.OUTSIDE_OF_ANY||i===Pe.LEFT_FOR_ANOTHER&&s!==R&&A.get(s).dropFromOthersDisabled){ve=!0,W=R;const l=A.get(R).items;l.splice(Ve,0,o),se(R,l,{trigger:Z.DRAGGED_LEFT_ALL,id:z[C],source:j.POINTER})}se(e.currentTarget,t,{trigger:Z.DRAGGED_LEFT,id:z[C],source:j.POINTER})}function an(e){const{items:t,dropFromOthersDisabled:n}=A.get(e.currentTarget);if(n&&e.currentTarget!==R)return;ve=!1;const{index:r}=e.detail.indexObj,o=He(t);t.splice(o,1),t.splice(r,0,pe),se(e.currentTarget,t,{trigger:Z.DRAGGED_OVER_INDEX,id:z[C],source:j.POINTER})}function Ge(e){e.preventDefault();const t=e.touches?e.touches[0]:e;B={x:t.clientX,y:t.clientY},k.style.transform=`translate3d(${B.x-re.x}px, ${B.y-re.y}px, 0)`}function me(){gt=!0,window.removeEventListener("mousemove",Ge),window.removeEventListener("touchmove",Ge),window.removeEventListener("mouseup",me),window.removeEventListener("touchend",me),or(),Xn(k),W||(W=R);let{items:e,type:t}=A.get(W);Fe(X.get(t),o=>A.get(o).dropTargetStyle,o=>A.get(o).dropTargetClasses);let n=He(e);n===-1&&(n=Ve),e=e.map(o=>o[ze]?z:o);function r(){pt(),ge(W,e,{trigger:ve?Z.DROPPED_OUTSIDE_OF_ANY:Z.DROPPED_INTO_ZONE,id:z[C],source:j.POINTER}),W!==R&&ge(R,A.get(R).items,{trigger:Z.DROPPED_INTO_ANOTHER,id:z[C],source:j.POINTER}),Qn(W.children[n]),cr()}lr(n,r)}function lr(e,t){const n=qt(W.children[e]),r={x:n.left-parseFloat(k.style.left),y:n.top-parseFloat(k.style.top)},{dropAnimationDurationMs:o}=A.get(W),i=`transform ${o}ms ease`;k.style.transition=k.style.transition?k.style.transition+","+i:i,k.style.transform=`translate3d(${r.x}px, ${r.y}px, 0)`,window.setTimeout(t,o)}function ar(e,t){Ie.push({dz:e,destroy:t}),window.requestAnimationFrame(()=>{on(e),document.body.appendChild(e)})}function cr(){k.remove(),Q.remove(),Ie.length&&(Ie.forEach(({dz:e,destroy:t})=>{t(),e.remove()}),Ie=[]),k=void 0,Q=void 0,z=void 0,Be=void 0,R=void 0,Ve=void 0,pe=void 0,W=void 0,re=void 0,B=void 0,de=!1,gt=!1,pt=void 0,ve=!1}function dr(e,t){let n=!1;const r={items:void 0,type:void 0,flipDurationMs:0,dragDisabled:!1,morphDisabled:!1,dropFromOthersDisabled:!1,dropTargetStyle:yt,dropTargetClasses:[],transformDraggedElement:()=>{},centreDraggedOnCursor:!1};let o=new Map;function i(){window.addEventListener("mousemove",c,{passive:!1}),window.addEventListener("touchmove",c,{passive:!1,capture:!1}),window.addEventListener("mouseup",l,{passive:!1}),window.addEventListener("touchend",l,{passive:!1})}function s(){window.removeEventListener("mousemove",c),window.removeEventListener("touchmove",c),window.removeEventListener("mouseup",l),window.removeEventListener("touchend",l)}function l(){s(),Q=void 0,re=void 0,B=void 0}function c(a){a.preventDefault();const p=a.touches?a.touches[0]:a;B={x:p.clientX,y:p.clientY},(Math.abs(B.x-re.x)>=_t||Math.abs(B.y-re.y)>=_t)&&(s(),u())}function d(a){if(a.target!==a.currentTarget&&(a.target.value!==void 0||a.target.isContentEditable)||a.button||de)return;a.stopPropagation();const p=a.touches?a.touches[0]:a;re={x:p.clientX,y:p.clientY},B={...re},Q=a.currentTarget,i()}function u(){de=!0;const a=o.get(Q);Ve=a,R=Q.parentElement;const p=R.getRootNode(),w=p.body||p,{items:v,type:S,centreDraggedOnCursor:N}=r;z={...v[a]},Be=S,pe={...z,[ze]:!0};const L={...pe,[C]:ct};k=Yn(Q,N&&B);function E(){k.parentElement?window.requestAnimationFrame(E):(w.appendChild(k),k.focus(),ir(),on(Q),w.appendChild(Q))}window.requestAnimationFrame(E),be(Array.from(X.get(r.type)).filter(g=>g===R||!A.get(g).dropFromOthersDisabled),g=>A.get(g).dropTargetStyle,g=>A.get(g).dropTargetClasses),v.splice(a,1,L),pt=er(R),se(R,v,{trigger:Z.DRAG_STARTED,id:z[C],source:j.POINTER}),window.addEventListener("mousemove",Ge,{passive:!1}),window.addEventListener("touchmove",Ge,{passive:!1,capture:!1}),window.addEventListener("mouseup",me,{passive:!1}),window.addEventListener("touchend",me,{passive:!1})}function f({items:a=void 0,flipDurationMs:p=0,type:w=tr,dragDisabled:v=!1,morphDisabled:S=!1,dropFromOthersDisabled:N=!1,dropTargetStyle:L=yt,dropTargetClasses:E=[],transformDraggedElement:g=()=>{},centreDraggedOnCursor:_=!1}){r.dropAnimationDurationMs=p,r.type&&w!==r.type&&vt(e,r.type),r.type=w,rr(e,w),r.items=[...a],r.dragDisabled=v,r.morphDisabled=S,r.transformDraggedElement=g,r.centreDraggedOnCursor=_,n&&de&&!gt&&(!$n(L,r.dropTargetStyle)||!Pn(E,r.dropTargetClasses))&&(Fe([e],()=>r.dropTargetStyle,()=>E),be([e],()=>L,()=>E)),r.dropTargetStyle=L,r.dropTargetClasses=[...E];function y(h,m){return A.get(h)?A.get(h)[m]:r[m]}n&&de&&r.dropFromOthersDisabled!==N&&(N?Fe([e],h=>y(h,"dropTargetStyle"),h=>y(h,"dropTargetClasses")):be([e],h=>y(h,"dropTargetStyle"),h=>y(h,"dropTargetClasses"))),r.dropFromOthersDisabled=N,A.set(e,r);const O=He(r.items);for(let h=0;h<e.children.length;h++){const m=e.children[h];if(Kn(m,v),h===O){r.transformDraggedElement(k,z,h),S||qn(k,m,B.x,B.y),Jn(m);continue}m.removeEventListener("mousedown",qe.get(m)),m.removeEventListener("touchstart",qe.get(m)),v||(m.addEventListener("mousedown",d),m.addEventListener("touchstart",d),qe.set(m,d)),o.set(m,h),n||(n=!0)}}return f(t),{update:a=>{f(a)},destroy:()=>{function a(){vt(e,A.get(e).type),A.delete(e)}de?ar(e,a):a()}}}const nt={DND_ZONE_ACTIVE:"dnd-zone-active",DND_ZONE_DRAG_DISABLED:"dnd-zone-drag-disabled"},cn={[nt.DND_ZONE_ACTIVE]:"Tab to one the items and press space-bar or enter to start dragging it",[nt.DND_ZONE_DRAG_DISABLED]:"This is a disabled drag and drop list"},ur="dnd-action-aria-alert";let b;function rt(){b||(b=document.createElement("div"),function(){b.id=ur,b.style.position="fixed",b.style.bottom="0",b.style.left="0",b.style.zIndex="-5",b.style.opacity="0",b.style.height="0",b.style.width="0",b.setAttribute("role","alert")}(),document.body.prepend(b),Object.entries(cn).forEach(([e,t])=>document.body.prepend(gr(e,t))))}function fr(){return dt?null:(document.readyState==="complete"?rt():window.addEventListener("DOMContentLoaded",rt),{...nt})}function hr(){dt||!b||(Object.keys(cn).forEach(e=>{var t;return(t=document.getElementById(e))==null?void 0:t.remove()}),b.remove(),b=void 0)}function gr(e,t){const n=document.createElement("div");return n.id=e,n.innerHTML=`<p>${t}</p>`,n.style.display="none",n.style.position="fixed",n.style.zIndex="-5",n}function he(e){if(dt)return;b||rt(),b.innerHTML="";const t=document.createTextNode(e);b.appendChild(t),b.style.display="none",b.style.display="inline"}const pr="--any--",wt={outline:"rgba(255, 255, 102, 0.7) solid 2px"};let V=!1,it,M,fe="",ce,q,ie="";const Ze=new WeakSet,Ot=new WeakMap,Tt=new WeakMap,ot=new Map,P=new Map,Y=new Map;let Ue;function mr(e,t){Y.size===0&&(Ue=fr(),window.addEventListener("keydown",dn),window.addEventListener("click",un)),Y.has(t)||Y.set(t,new Set),Y.get(t).has(e)||(Y.get(t).add(e),Yt())}function bt(e,t){M===e&&_e(),Y.get(t).delete(e),Xt(),Y.get(t).size===0&&Y.delete(t),Y.size===0&&(window.removeEventListener("keydown",dn),window.removeEventListener("click",un),Ue=void 0,hr())}function dn(e){if(!!V)switch(e.key){case"Escape":{_e();break}}}function un(){!V||Ze.has(document.activeElement)||_e()}function Er(e){if(!V)return;const t=e.currentTarget;if(t===M)return;fe=t.getAttribute("aria-label")||"";const{items:n}=P.get(M),r=n.find(d=>d[C]===q),o=n.indexOf(r),i=n.splice(o,1)[0],{items:s,autoAriaDisabled:l}=P.get(t);t.getBoundingClientRect().top<M.getBoundingClientRect().top||t.getBoundingClientRect().left<M.getBoundingClientRect().left?(s.push(i),l||he(`Moved item ${ie} to the end of the list ${fe}`)):(s.unshift(i),l||he(`Moved item ${ie} to the beginning of the list ${fe}`)),ge(M,n,{trigger:Z.DROPPED_INTO_ANOTHER,id:q,source:j.KEYBOARD}),ge(t,s,{trigger:Z.DROPPED_INTO_ZONE,id:q,source:j.KEYBOARD}),M=t}function fn(){ot.forEach(({update:e},t)=>e(P.get(t)))}function _e(e=!0){P.get(M).autoAriaDisabled||he(`Stopped dragging item ${ie}`),Ze.has(document.activeElement)&&document.activeElement.blur(),e&&se(M,P.get(M).items,{trigger:Z.DRAG_STOPPED,id:q,source:j.KEYBOARD}),Fe(Y.get(it),t=>P.get(t).dropTargetStyle,t=>P.get(t).dropTargetClasses),ce=null,q=null,ie="",it=null,M=null,fe="",V=!1,fn()}function Dr(e,t){const n={items:void 0,type:void 0,dragDisabled:!1,zoneTabIndex:0,dropFromOthersDisabled:!1,dropTargetStyle:wt,dropTargetClasses:[],autoAriaDisabled:!1};function r(u,f,a){u.length<=1||u.splice(a,1,u.splice(f,1,u[a])[0])}function o(u){switch(u.key){case"Enter":case" ":{if((u.target.disabled!==void 0||u.target.href||u.target.isContentEditable)&&!Ze.has(u.target))return;u.preventDefault(),u.stopPropagation(),V?_e():i(u);break}case"ArrowDown":case"ArrowRight":{if(!V)return;u.preventDefault(),u.stopPropagation();const{items:f}=P.get(e),a=Array.from(e.children),p=a.indexOf(u.currentTarget);p<a.length-1&&(n.autoAriaDisabled||he(`Moved item ${ie} to position ${p+2} in the list ${fe}`),r(f,p,p+1),ge(e,f,{trigger:Z.DROPPED_INTO_ZONE,id:q,source:j.KEYBOARD}));break}case"ArrowUp":case"ArrowLeft":{if(!V)return;u.preventDefault(),u.stopPropagation();const{items:f}=P.get(e),p=Array.from(e.children).indexOf(u.currentTarget);p>0&&(n.autoAriaDisabled||he(`Moved item ${ie} to position ${p} in the list ${fe}`),r(f,p,p-1),ge(e,f,{trigger:Z.DROPPED_INTO_ZONE,id:q,source:j.KEYBOARD}));break}}}function i(u){l(u.currentTarget),M=e,it=n.type,V=!0;const f=Array.from(Y.get(n.type)).filter(a=>a===M||!P.get(a).dropFromOthersDisabled);if(be(f,a=>P.get(a).dropTargetStyle,a=>P.get(a).dropTargetClasses),!n.autoAriaDisabled){let a=`Started dragging item ${ie}. Use the arrow keys to move it within its list ${fe}`;f.length>1&&(a+=", or tab to another list in order to move the item into it"),he(a)}se(e,P.get(e).items,{trigger:Z.DRAG_STARTED,id:q,source:j.KEYBOARD}),fn()}function s(u){!V||u.currentTarget!==ce&&(u.stopPropagation(),_e(!1),i(u))}function l(u){const{items:f}=P.get(e),a=Array.from(e.children),p=a.indexOf(u);ce=u,ce.tabIndex=0,q=f[p][C],ie=a[p].getAttribute("aria-label")||""}function c({items:u=[],type:f=pr,dragDisabled:a=!1,zoneTabIndex:p=0,dropFromOthersDisabled:w=!1,dropTargetStyle:v=wt,dropTargetClasses:S=[],autoAriaDisabled:N=!1}){n.items=[...u],n.dragDisabled=a,n.dropFromOthersDisabled=w,n.zoneTabIndex=p,n.dropTargetStyle=v,n.dropTargetClasses=S,n.autoAriaDisabled=N,n.type&&f!==n.type&&bt(e,n.type),n.type=f,mr(e,f),N||(e.setAttribute("aria-disabled",a),e.setAttribute("role","list"),e.setAttribute("aria-describedby",a?Ue.DND_ZONE_DRAG_DISABLED:Ue.DND_ZONE_ACTIVE)),P.set(e,n),V?e.tabIndex=e===M||ce.contains(e)||n.dropFromOthersDisabled||M&&n.type!==P.get(M).type?-1:0:e.tabIndex=n.zoneTabIndex,e.addEventListener("focus",Er);for(let L=0;L<e.children.length;L++){const E=e.children[L];Ze.add(E),E.tabIndex=V?-1:0,N||E.setAttribute("role","listitem"),E.removeEventListener("keydown",Ot.get(E)),E.removeEventListener("click",Tt.get(E)),a||(E.addEventListener("keydown",o),Ot.set(E,o),E.addEventListener("click",s),Tt.set(E,s)),V&&n.items[L][C]===q&&(ce=E,ce.tabIndex=0,E.focus())}}c(t);const d={update:u=>{c(u)},destroy:()=>{bt(e,n.type),P.delete(e),ot.delete(e)}};return ot.set(e,d),d}function hn(e,t){It(t);const n=dr(e,t),r=Dr(e,t);return{update:o=>{It(o),n.update(o),r.update(o)},destroy:()=>{n.destroy(),r.destroy()}}}function It(e){const{items:t,flipDurationMs:n,type:r,dragDisabled:o,morphDisabled:i,dropFromOthersDisabled:s,zoneTabIndex:l,dropTargetStyle:c,dropTargetClasses:d,transformDraggedElement:u,autoAriaDisabled:f,centreDraggedOnCursor:a,...p}=e;if(Object.keys(p).length>0&&console.warn("dndzone will ignore unknown options",p),!t)throw new Error("no 'items' key provided to dndzone");const w=t.find(v=>!{}.hasOwnProperty.call(v,C));if(w)throw new Error(`missing '${C}' property for item ${Xe(w)}`);if(d&&!Array.isArray(d))throw new Error(`dropTargetClasses should be an array but instead it is a ${typeof d}, ${Xe(d)}`);if(l&&!_r(l))throw new Error(`zoneTabIndex should be a number but instead it is a ${typeof l}, ${Xe(l)}`)}function _r(e){return!isNaN(e)&&function(t){return(t|0)===t}(parseFloat(e))}let Oe;const yr=new Uint8Array(16);function vr(){if(!Oe&&(Oe=typeof crypto<"u"&&crypto.getRandomValues&&crypto.getRandomValues.bind(crypto),!Oe))throw new Error("crypto.getRandomValues() not supported. See https://github.com/uuidjs/uuid#getrandomvalues-not-supported");return Oe(yr)}const $=[];for(let e=0;e<256;++e)$.push((e+256).toString(16).slice(1));function wr(e,t=0){return($[e[t+0]]+$[e[t+1]]+$[e[t+2]]+$[e[t+3]]+"-"+$[e[t+4]]+$[e[t+5]]+"-"+$[e[t+6]]+$[e[t+7]]+"-"+$[e[t+8]]+$[e[t+9]]+"-"+$[e[t+10]]+$[e[t+11]]+$[e[t+12]]+$[e[t+13]]+$[e[t+14]]+$[e[t+15]]).toLowerCase()}const Or=typeof crypto<"u"&&crypto.randomUUID&&crypto.randomUUID.bind(crypto),At={randomUUID:Or};function Tr(e,t,n){if(At.randomUUID&&!t&&!e)return At.randomUUID();e=e||{};const r=e.random||(e.rng||vr)();if(r[6]=r[6]&15|64,r[8]=r[8]&63|128,t){n=n||0;for(let o=0;o<16;++o)t[n+o]=r[o];return t}return wr(r)}function gn(e,{from:t,to:n},r={}){const o=getComputedStyle(e),i=o.transform==="none"?"":o.transform,[s,l]=o.transformOrigin.split(" ").map(parseFloat),c=t.left+t.width*s/n.width-(n.left+s),d=t.top+t.height*l/n.height-(n.top+l),{delay:u=0,duration:f=p=>Math.sqrt(p)*120,easing:a=mn}=r;return{delay:u,duration:st(f)?f(Math.sqrt(c*c+d*d)):f,easing:a,css:(p,w)=>{const v=w*c,S=w*d,N=p+w*t.width/n.width,L=p+w*t.height/n.height;return`transform: ${i} translate(${v}px, ${S}px) scale(${N}, ${L});`}}}function xt(e,t,n){const r=e.slice();return r[2]=t[n],r}function Rt(e,t,n){const r=e.slice();return r[5]=t[n],r}function Nt(e){let t,n,r;return{c(){t=F("img"),this.h()},l(o){t=G(o,"IMG",{src:!0,alt:!0,class:!0}),this.h()},h(){xe(t.src,n=e[5][1].FaceURL)||T(t,"src",n),T(t,"alt",r=e[0].Nickname.split(`
`)[0]),T(t,"class","svelte-1emkmrw")},m(o,i){te(o,t,i)},p(o,i){i&1&&!xe(t.src,n=o[5][1].FaceURL)&&T(t,"src",n),i&1&&r!==(r=o[0].Nickname.split(`
`)[0])&&T(t,"alt",r)},d(o){o&&x(t)}}}function Lt(e){let t,n;return{c(){t=F("img"),this.h()},l(r){t=G(r,"IMG",{src:!0,alt:!0,class:!0}),this.h()},h(){xe(t.src,n=e[2].CustomDecal.ImageURL)||T(t,"src",n),T(t,"alt","Decal"),T(t,"class","svelte-1emkmrw")},m(r,o){te(r,t,o)},p(r,o){o&1&&!xe(t.src,n=r[2].CustomDecal.ImageURL)&&T(t,"src",n)},d(r){r&&x(t)}}}function br(e){var c;let t,n,r,o=[...Object.entries(e[0].CustomDeck)],i=[];for(let d=0;d<o.length;d+=1)i[d]=Nt(Rt(e,o,d));let s=(c=e[0].AttachedDecals)!=null?c:[],l=[];for(let d=0;d<s.length;d+=1)l[d]=Lt(xt(e,s,d));return{c(){t=F("div");for(let d=0;d<i.length;d+=1)i[d].c();n=K();for(let d=0;d<l.length;d+=1)l[d].c();this.h()},l(d){t=G(d,"DIV",{class:!0,style:!0});var u=H(t);for(let f=0;f<i.length;f+=1)i[f].l(u);n=J(u);for(let f=0;f<l.length;f+=1)l[f].l(u);u.forEach(x),this.h()},h(){T(t,"class","grid svelte-1emkmrw"),T(t,"style",r=`--visible: ${e[1]?"100%":"30%"}`)},m(d,u){te(d,t,u);for(let f=0;f<i.length;f+=1)i[f].m(t,null);I(t,n);for(let f=0;f<l.length;f+=1)l[f].m(t,null)},p(d,[u]){var f;if(u&1){o=[...Object.entries(d[0].CustomDeck)];let a;for(a=0;a<o.length;a+=1){const p=Rt(d,o,a);i[a]?i[a].p(p,u):(i[a]=Nt(p),i[a].c(),i[a].m(t,n))}for(;a<i.length;a+=1)i[a].d(1);i.length=o.length}if(u&1){s=(f=d[0].AttachedDecals)!=null?f:[];let a;for(a=0;a<s.length;a+=1){const p=xt(d,s,a);l[a]?l[a].p(p,u):(l[a]=Lt(p),l[a].c(),l[a].m(t,null))}for(;a<l.length;a+=1)l[a].d(1);l.length=s.length}u&2&&r!==(r=`--visible: ${d[1]?"100%":"30%"}`)&&T(t,"style",r)},i:Ae,o:Ae,d(d){d&&x(t),Ke(i,d),Ke(l,d)}}}function Ir(e,t,n){let{card:r}=t,{highlighted:o=!1}=t;return e.$$set=i=>{"card"in i&&n(0,r=i.card),"highlighted"in i&&n(1,o=i.highlighted)},[r,o]}class pn extends Ft{constructor(t){super(),Gt(this,t,Ir,br,Zt,{card:0,highlighted:1})}}function St(e,t,n){const r=e.slice();return r[17]=t[n][0],r[18]=t[n][1],r}function Ct(e,t,n){const r=e.slice();return r[21]=t[n],r}function $t(e,t,n){const r=e.slice();return r[24]=t[n],r}function Pt(e,t){let n,r,o,i,s=Ae,l;return r=new pn({props:{card:t[24].card,highlighted:t[24].highlighted}}),{key:e,first:null,c(){n=F("div"),Le(r.$$.fragment),o=K(),this.h()},l(c){n=G(c,"DIV",{});var d=H(n);Se(r.$$.fragment,d),o=J(d),d.forEach(x),this.h()},h(){this.first=n},m(c,d){te(c,n,d),Ce(r,n,null),I(n,o),l=!0},p(c,d){t=c;const u={};d&2&&(u.card=t[24].card),d&2&&(u.highlighted=t[24].highlighted),r.$set(u)},r(){i=n.getBoundingClientRect()},f(){zt(n),s()},a(){s(),s=Bt(n,i,gn,{duration:300})},i(c){l||(ee(r.$$.fragment,c),l=!0)},o(c){oe(r.$$.fragment,c),l=!1},d(c){c&&x(n),$e(r)}}}function Ar(e){let t=e[21].card.Nickname+"",n;return{c(){n=Re(t)},l(r){n=Ne(r,t)},m(r,o){te(r,n,o)},p(r,o){o&4&&t!==(t=r[21].card.Nickname+"")&&Vt(n,t)},d(r){r&&x(n)}}}function xr(e){let t,n,r,o;return t=new Dn({props:{$$slots:{default:[Ar]},$$scope:{ctx:e}}}),r=new pn({props:{card:e[21].card,highlighted:e[21].highlighted}}),{c(){Le(t.$$.fragment),n=K(),Le(r.$$.fragment)},l(i){Se(t.$$.fragment,i),n=J(i),Se(r.$$.fragment,i)},m(i,s){Ce(t,i,s),te(i,n,s),Ce(r,i,s),o=!0},p(i,s){const l={};s&134217732&&(l.$$scope={dirty:s,ctx:i}),t.$set(l);const c={};s&4&&(c.card=i[21].card),s&4&&(c.highlighted=i[21].highlighted),r.$set(c)},i(i){o||(ee(t.$$.fragment,i),ee(r.$$.fragment,i),o=!0)},o(i){oe(t.$$.fragment,i),oe(r.$$.fragment,i),o=!1},d(i){$e(t,i),i&&x(n),$e(r,i)}}}function kt(e,t){let n,r,o,i,s=Ae,l;return r=new En({props:{$$slots:{default:[xr]},$$scope:{ctx:t}}}),{key:e,first:null,c(){n=F("div"),Le(r.$$.fragment),o=K(),this.h()},l(c){n=G(c,"DIV",{style:!0});var d=H(n);Se(r.$$.fragment,d),o=J(d),d.forEach(x),this.h()},h(){Te(n,"height","min-content"),this.first=n},m(c,d){te(c,n,d),Ce(r,n,null),I(n,o),l=!0},p(c,d){t=c;const u={};d&134217732&&(u.$$scope={dirty:d,ctx:t}),r.$set(u)},r(){i=n.getBoundingClientRect()},f(){zt(n),s()},a(){s(),s=Bt(n,i,gn,{duration:300})},i(c){l||(ee(r.$$.fragment,c),l=!0)},o(c){oe(r.$$.fragment,c),l=!1},d(c){c&&x(n),$e(r)}}}function Mt(e){let t,n,r,o=e[17]+"",i,s,l,c=[],d=new Map,u,f,a,p,w,v=e[18];const S=E=>E[21].id;for(let E=0;E<v.length;E+=1){let g=Ct(e,v,E),_=S(g);d.set(_,c[E]=kt(_,g))}function N(...E){return e[14](e[17],...E)}function L(...E){return e[15](e[17],...E)}return{c(){t=F("div"),n=F("div"),r=Re("Group "),i=Re(o),s=K(),l=F("section");for(let E=0;E<c.length;E+=1)c[E].c();f=K(),this.h()},l(E){t=G(E,"DIV",{class:!0});var g=H(t);n=G(g,"DIV",{class:!0});var _=H(n);r=Ne(_,"Group "),i=Ne(_,o),_.forEach(x),s=J(g),l=G(g,"SECTION",{class:!0});var y=H(l);for(let O=0;O<c.length;O+=1)c[O].l(y);y.forEach(x),f=J(g),g.forEach(x),this.h()},h(){T(n,"class","text-xl"),T(l,"class","grouping svelte-1oxp21m"),T(t,"class","")},m(E,g){te(E,t,g),I(t,n),I(n,r),I(n,i),I(t,s),I(t,l);for(let _=0;_<c.length;_+=1)c[_].m(l,null);I(t,f),a=!0,p||(w=[Ut(u=hn.call(null,l,{items:e[18],flipDurationMs:300})),ne(l,"consider",N),ne(l,"finalize",L)],p=!0)},p(E,g){if(e=E,(!a||g&4)&&o!==(o=e[17]+"")&&Vt(i,o),g&4){v=e[18],Qe();for(let _=0;_<c.length;_+=1)c[_].r();c=jt(c,g,S,1,e,v,d,l,Ht,kt,null,Ct);for(let _=0;_<c.length;_+=1)c[_].a();Je()}u&&st(u.update)&&g&4&&u.update.call(null,{items:e[18],flipDurationMs:300})},i(E){if(!a){for(let g=0;g<v.length;g+=1)ee(c[g]);a=!0}},o(E){for(let g=0;g<c.length;g+=1)oe(c[g]);a=!1},d(E){E&&x(t);for(let g=0;g<c.length;g+=1)c[g].d();p=!1,Wt(w)}}}function Rr(e){let t,n,r,o,i,s,l,c,d,u,f=[],a=new Map,p,w,v,S,N,L,E=e[1];const g=h=>h[24].id;for(let h=0;h<E.length;h+=1){let m=$t(e,E,h),D=g(m);a.set(D,f[h]=Pt(D,m))}let _=Object.entries(e[2]),y=[];for(let h=0;h<_.length;h+=1)y[h]=Mt(St(e,_,h));const O=h=>oe(y[h],1,1,()=>{y[h]=null});return{c(){t=F("div"),n=F("div"),r=F("input"),o=K(),i=F("button"),s=Re("Export"),l=K(),c=F("input"),d=K(),u=F("section");for(let h=0;h<f.length;h+=1)f[h].c();w=K(),v=F("div");for(let h=0;h<y.length;h+=1)y[h].c();this.h()},l(h){t=G(h,"DIV",{class:!0});var m=H(t);n=G(m,"DIV",{class:!0});var D=H(n);r=G(D,"INPUT",{type:!0,accept:!0}),o=J(D),i=G(D,"BUTTON",{});var U=H(i);s=Ne(U,"Export"),U.forEach(x),l=J(D),c=G(D,"INPUT",{type:!0}),d=J(D),u=G(D,"SECTION",{class:!0,style:!0});var Ye=H(u);for(let le=0;le<f.length;le+=1)f[le].l(Ye);Ye.forEach(x),D.forEach(x),w=J(m),v=G(m,"DIV",{class:!0});var we=H(v);for(let le=0;le<y.length;le+=1)y[le].l(we);we.forEach(x),m.forEach(x),this.h()},h(){T(r,"type","file"),T(r,"accept","text/json"),T(c,"type","text"),T(u,"class","flex flex-wrap gap-2"),Te(u,"min-height","120px"),Te(u,"max-height","900px"),Te(u,"overflow-y","scroll"),T(n,"class","sidebar flex flex-col svelte-1oxp21m"),T(v,"class","grid overflow-scroll svelte-1oxp21m"),T(t,"class","parent svelte-1oxp21m")},m(h,m){te(h,t,m),I(t,n),I(n,r),I(n,o),I(n,i),I(i,s),I(n,l),I(n,c),I(n,d),I(n,u);for(let D=0;D<f.length;D+=1)f[D].m(u,null);I(t,w),I(t,v);for(let D=0;D<y.length;D+=1)y[D].m(v,null);S=!0,N||(L=[ne(r,"change",e[8]),ne(r,"change",e[9]),ne(i,"click",e[10]),ne(c,"change",e[11]),Ut(p=hn.call(null,u,{items:e[1],flipDurationMs:300})),ne(u,"consider",e[12]),ne(u,"finalize",e[13])],N=!0)},p(h,[m]){if(m&2){E=h[1],Qe();for(let D=0;D<f.length;D+=1)f[D].r();f=jt(f,m,g,1,h,E,a,u,Ht,Pt,null,$t);for(let D=0;D<f.length;D+=1)f[D].a();Je()}if(p&&st(p.update)&&m&2&&p.update.call(null,{items:h[1],flipDurationMs:300}),m&36){_=Object.entries(h[2]);let D;for(D=0;D<_.length;D+=1){const U=St(h,_,D);y[D]?(y[D].p(U,m),ee(y[D],1)):(y[D]=Mt(U),y[D].c(),ee(y[D],1),y[D].m(v,null))}for(Qe(),D=_.length;D<y.length;D+=1)O(D);Je()}},i(h){if(!S){for(let m=0;m<E.length;m+=1)ee(f[m]);for(let m=0;m<_.length;m+=1)ee(y[m]);S=!0}},o(h){for(let m=0;m<f.length;m+=1)oe(f[m]);y=y.filter(Boolean);for(let m=0;m<y.length;m+=1)oe(y[m]);S=!1},d(h){h&&x(t);for(let m=0;m<f.length;m+=1)f[m].d();Ke(y,h),N=!1,Wt(L)}}}function Nr(e,t,n){let r,{data:i}=t;function s(){Promise.allSettled(Array.from(l).map(g=>g.text().then(_=>{let y=JSON.parse(_),O=[];for(const h of y.ObjectStates){if(h.Name==="Bag")for(const m of h.ContainedObjects)m.Name==="Deck"&&O.push(m.ContainedObjects),m.Name==="Card"&&O.push([m]);h.Name==="Deck"&&O.push(h.ContainedObjects),h.Name==="Card"&&O.push([h])}return O}))).then(g=>{g.forEach(_=>{_.status==="fulfilled"&&_.value.map(y=>{n(2,f[r]=y.map(O=>({id:Tr(),card:O,highlighted:!0})),f),r=r+1})})})}let l,c=[];function d(){var m;if(console.log(Object.fromEntries(c.map((D,U)=>[U+1,Object.entries(D.card.CustomDeck)[0][1]]))),c.length<2)return alert("Don't export with one or fewer cards, it breaks things.");const g={ObjectStates:[{Name:"Deck",ColorDiffuse:{b:0,g:0,r:0},ContainedObjects:c.map((D,U)=>({...D.card,CardID:(U+1)*100,CustomDeck:Object.fromEntries(Object.entries(D.card.CustomDeck).map(([Ye,we])=>[U+1,we]))})),CustomDeck:Object.fromEntries(c.map((D,U)=>[U+1,Object.entries(D.card.CustomDeck)[0][1]])),DeckIDs:c.map((D,U)=>(U+1)*100),Nickname:"",Transform:{posX:0,posY:0,posZ:0,rotX:0,rotY:0,rotZ:0,scaleX:1,scaleY:1,scaleZ:1}}]},_=(m=`${prompt("File name:")}.json`)!=null?m:"myCards.json";var y=new Blob([JSON.stringify(g)],{type:"text/json"}),O=document.createElement("a"),h=URL.createObjectURL(y);O.href=h,O.download=_,document.body.appendChild(O),O.click(),setTimeout(function(){document.body.removeChild(O),window.URL.revokeObjectURL(h)},0)}function u(g,_){_===void 0&&n(1,c=g.detail.items),_!==void 0&&n(2,f[_]=g.detail.items,f)}let f={};function a(){l=this.files,n(0,l)}const p=()=>{s()},w=()=>d(),v=g=>{n(2,f=Object.fromEntries(Object.entries(f).map(([_,y])=>[_,y.map(O=>({...O,highlighted:g.currentTarget.value===""||O.card.Description.includes(g.currentTarget.value)}))])))},S=g=>u(g),N=g=>u(g),L=(g,_)=>u(_,g),E=(g,_)=>u(_,g);return e.$$set=g=>{"data"in g&&n(7,i=g.data)},r=0,[l,c,f,s,d,u,!0,i,a,p,w,v,S,N,L,E]}class Cr extends Ft{constructor(t){super(),Gt(this,t,Nr,Rr,Zt,{prerender:6,data:7})}get prerender(){return this.$$.ctx[6]}}export{Cr as default};