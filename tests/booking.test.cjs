const vm=require('node:vm'),fs=require('node:fs'),assert=require('node:assert/strict');
const elements=new Map();function elem(s){if(!elements.has(s))elements.set(s,{innerHTML:'',textContent:'',outerHTML:'',value:'',style:{},classList:{toggle(){}},insertAdjacentHTML(){},scrollIntoView(){},close(){},showModal(){}});return elements.get(s)}
let stored=null;const ctx={document:{querySelector:elem,querySelectorAll:()=>[]},localStorage:{getItem:()=>stored,setItem:(k,v)=>stored=v},window:{scrollTo(){},addEventListener(){}},setTimeout:()=>0,clearTimeout(){},console,assert};vm.createContext(ctx);for(const file of ['app.js','upgrade.js'])vm.runInContext(fs.readFileSync('dist/'+file,'utf8'),ctx);
vm.runInContext(`
go=()=>{};renderBookings=()=>{};renderAdmin=()=>{};toast=()=>{};closeModal=()=>{};
current={id:1,name:'A'};db.users=[current,{id:2,name:'B'},{id:3,name:'C'}];db.bookings=[];db.orders=[];db.showQueues={};db.stack=[];db.nextBooking=101;db.nextOrder=1001;
chosenDate=dateChoices()[2];chosenTime='18:00';let m=movie(1),m2=movie(2);m.seats=10;
cart=[{movie:m.id,title:m.name,date:chosenDate,time:chosenTime,seats:[1,2,3],price:m.price},{movie:m2.id,title:m2.name,date:chosenDate,time:'21:30',seats:[4,5],price:m2.price}];snackQty=2;discountApplied=true;
assert.equal(totals().total,(3*m.price+2*m2.price)*.9+360);
let o=commitOrder('UPI');assert.equal(o.bookings.length,2);assert.equal(db.bookings.reduce((s,b)=>s+bSeats(b).length,0),5);assert.equal(cart.length,0);assert.equal(available(m),7);assert.equal(takenSeats(m.id,chosenDate,'14:00').length,0);
cart=[{movie:m.id,title:m.name,date:chosenDate,time:chosenTime,seats:[1],price:m.price}];assert.match(cartError(),/no longer/);let before=db.bookings.length;assert.throws(()=>commitOrder('Cash'));assert.equal(db.bookings.length,before);cart=[];
let b=db.bookings[0];db.showQueues[keyFor(m.id)]=[{user:2,count:8},{user:3,count:1}];allocateShow(m.id,chosenDate,chosenTime);assert.equal(db.showQueues[keyFor(m.id)].length,2);cancelOrder(o.id);assert.equal(o.payment,'Refunded');assert.equal(db.stack.length,2);let allocations=db.bookings.filter(x=>!x.order);assert.equal(allocations.length,2);assert.equal(allocations[0].user,2);assert.equal(allocations[0].seats.length,8);assert.equal(allocations[1].user,3);assert.equal(available(m),1);assert.equal(allocations[0].payment,'Pending');
admin=true;finishSettlement(allocations[0].id);assert.equal(allocations[0].payment,'Paid');assert.equal(allocations[0].paidAmount,8*m.price);current=db.users[1];cancelBooking(allocations[0].id);assert.equal(allocations[0].payment,'Refunded');assert.equal(available(m),9);
selectedMovie=m2.id;cart=[];let suggested=bestSeats(m2,3,chosenDate,chosenTime);assert.equal(suggested.length,3);assert.equal(suggested[2]-suggested[0],2);assert.equal(new Set(suggested.map(n=>Math.floor((n-1)/5))).size,1);
let preserved=JSON.parse(localStorage.getItem('cineseat-v1'));assert.ok(preserved.orders.length);assert.equal(db.bookings[0].status,'Cancelled');
console.log('PASS: 22 assertions covering multi-show orders, multiple seats, discounts, snacks, conflict rejection, show isolation, group FIFO, cancellation/refund, counter settlement, smart seats and persistence.');
`,ctx);
