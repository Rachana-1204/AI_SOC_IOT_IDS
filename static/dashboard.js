let attackCount = 0;
let safeCount = 0;

// =====================================================
// CHARTS
// =====================================================

const lineChart = new Chart(

document.getElementById('lineChart'),

{
type:'line',

data:{

labels:[],

datasets:[{

label:'Threats',

data:[],

borderColor:'#ef4444',

backgroundColor:'rgba(239,68,68,0.2)',

fill:true,

tension:0.4

}]
}
});

const pieChart = new Chart(

document.getElementById('pieChart'),

{
type:'doughnut',

data:{

labels:['Safe','Attack'],

datasets:[{

data:[0,0],

backgroundColor:[
'#22c55e',
'#ef4444'
]

}]
}
});

// =====================================================
// LIVE TRAFFIC
// =====================================================

async function loadLive(){

const response = await fetch('/live');

const data = await response.json();

let html = '';

let terminal = '';

attackCount = 0;
safeCount = 0;

data.forEach(item=>{

if(item.status==="Attack Detected"){
attackCount++;
}else{
safeCount++;
}

let cls =
item.status==="Attack Detected"
? "danger"
: "safe";

let badge =
item.status==="Attack Detected"
? "red"
: "green";

html += `

<div class="threat-card ${cls}">

<div class="top">

<h3>${item.attack}</h3>

<div class="badge ${badge}">
${item.severity}
</div>

</div>

<p>
<b>Device:</b>
${item.device}
</p>

<p>
<b>Country:</b>
${item.country}
</p>

<p>
<b>AI Confidence:</b>
${item.confidence}%
</p>

<p>
${item.explanation}
</p>

</div>
`;

terminal += `
[${item.time}]
${item.attack}
detected on
${item.device}
<br>
`;
});

document.getElementById(
'live-feed'
).innerHTML = html;

document.getElementById(
'terminal'
).innerHTML = terminal;

document.getElementById(
'attacks'
).innerText = attackCount;

document.getElementById(
'safe'
).innerText = safeCount;

document.getElementById(
'total'
).innerText = attackCount + safeCount;

// CHARTS

lineChart.data.labels.push(
attackCount + safeCount
);

lineChart.data.datasets[0].data.push(
attackCount
);

lineChart.update();

pieChart.data.datasets[0].data = [
safeCount,
attackCount
];

pieChart.update();
}

// =====================================================
// SHAP
// =====================================================

async function loadShap(){

const response = await fetch('/shap');

const data = await response.json();

let html = '';

let top = '';

data.forEach((item,index)=>{

if(index===0){
top = item.feature;
}

html += `

<div class="shap-row">

<div>

${item.feature}

</div>

<div class="bar-bg">

<div class="bar"
style="width:${item.importance*100}%">

</div>

</div>

<div>

${item.importance}

</div>

</div>
`;
});

document.getElementById(
'shap-box'
).innerHTML = html;

document.getElementById(
'ai-reason'
).innerHTML = `

AI detected abnormal behavior because
<b>${top}</b>
showed highly suspicious activity
compared to learned IoT patterns.
The ML models identified unusual
traffic behavior consistent with
potential cyber attacks.
`;
}

loadLive();
loadShap();

setInterval(loadLive,3000);
setInterval(loadShap,5000);