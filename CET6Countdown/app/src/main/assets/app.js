
(() => {
  "use strict";
  const TASKS_KEY = "cet6.v2.tasks";
  const CONFIG_KEY = "cet6.v2.config";
  const DONE_PREFIX = "cet6.v2.done.";
  const defaults = [
    { id:"listening",title:"英语六级听力",category:"听力",minutes:30 },
    { id:"reading",title:"阅读理解练习",category:"阅读",minutes:25 },
    { id:"words",title:"核心词汇复习",category:"词汇",minutes:20 },
    { id:"writing",title:"写作 / 翻译训练",category:"写作翻译",minutes:15 }
  ];
  const defaultConfig = { goal:550,exam:"2026-12-12T15:00",theme:"midnight" };
  const icons = { "听力":"🎧","阅读":"📖","词汇":"📝","写作翻译":"✍️","其他":"✦" };
  const $ = id => document.getElementById(id);
  const safeRead = (key, fallback) => {
    try { const data=JSON.parse(localStorage.getItem(key)); return data===null?fallback:data; }
    catch (e) { return fallback; }
  };
  const save = (key, value) => {
    try { localStorage.setItem(key,JSON.stringify(value)); return true; }
    catch (e) { notify("保存失败：手机存储不可用"); return false; }
  };
  const esc = s => String(s).replace(/[&<>"']/g,ch=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[ch]));
  const pad = n => String(n).padStart(2,"0");
  const validExam = s => /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(s) && Number.isFinite(Date.parse(s+":00+08:00"));
  const todayBJ = () => {
    const parts=new Intl.DateTimeFormat("en-US",{timeZone:"Asia/Shanghai",year:"numeric",month:"2-digit",day:"2-digit"}).formatToParts(new Date());
    const obj={};parts.forEach(p=>obj[p.type]=p.value);
    return obj.year+"-"+obj.month+"-"+obj.day;
  };
  function normalizeTasks(raw){
    if(!Array.isArray(raw))return defaults.map(t=>({...t}));
    return raw.filter(t=>t&&typeof t.id==="string"&&typeof t.title==="string"&&t.title.trim())
      .slice(0,80).map(t=>({id:t.id.slice(0,100),title:t.title.slice(0,36),category:icons[t.category]?t.category:"其他",minutes:Math.max(1,Math.min(600,Number(t.minutes)||30))}));
  }
  let config = {...defaultConfig,...safeRead(CONFIG_KEY,{})};
  if(!validExam(config.exam))config.exam=defaultConfig.exam;
  if(!Number.isFinite(Number(config.goal))||Number(config.goal)<1||Number(config.goal)>710)config.goal=550;
  if(!["midnight","violet","light"].includes(config.theme))config.theme="midnight";
  let tasks = normalizeTasks(safeRead(TASKS_KEY,null));
  let currentDate=todayBJ();
  let done = safeRead(DONE_PREFIX+currentDate,{});
  if(typeof done!=="object"||!done||Array.isArray(done))done={};
  // Preserve checkmarks made in the earlier, fixed-task application on upgrade.
  if(!localStorage.getItem(DONE_PREFIX+currentDate)){
    for(const t of defaults){if(localStorage.getItem("c6-"+currentDate+"-"+t.id)==="1")done[t.id]=true;}
    if(Object.values(done).some(Boolean))save(DONE_PREFIX+currentDate,done);
  }
  let editId=null;
  let selectedTheme=config.theme;
  let toastTimer;
  function notify(message) {
    const el=$("toast"); if(!el)return;
    el.textContent=message;el.classList.add("show");
    clearTimeout(toastTimer);toastTimer=setTimeout(()=>el.classList.remove("show"),2300);
  }
  function markCount(){return tasks.filter(t=>done[t.id]===true).length;}
  function syncNative(){
    try{
      if(window.CETBridge&&typeof window.CETBridge.syncWidget==="function"){
        window.CETBridge.syncWidget(String(config.exam),String(config.goal),markCount(),tasks.length,String(config.theme));
      }
    }catch(e){}
  }
  function checkDate(){
    const key=todayBJ();
    if(key!==currentDate){
      currentDate=key;done=safeRead(DONE_PREFIX+currentDate,{});
      if(!done||typeof done!=="object"||Array.isArray(done))done={};
      render();syncNative();
    }
  }
  function streakDays(){
    let count=0;
    const start=new Date(currentDate+"T12:00:00+08:00").getTime();
    for(let offset=0;offset<366;offset++){
      const day = new Date(start-offset*86400000).toISOString().slice(0,10);
      const flags=offset===0?done:safeRead(DONE_PREFIX+day,{});
      if(flags&&typeof flags==="object"&&Object.values(flags).some(Boolean))count++;
      else if(offset===0)continue;
      else break;
    }
    return count;
  }
  function taskMarkup(t){
    const completed=done[t.id]===true;
    const id=esc(t.id),name=esc(t.title),category=esc(t.category);
    return '<div class="task'+(completed?' done':'')+'">'+
      '<button class="task-check" data-check="'+id+'" aria-label="'+(completed?'取消完成':'标记完成')+'">'+(completed?'✓':'')+'</button>'+
      '<span class="task-emoji">'+(icons[t.category]||"✦")+'</span>'+
      '<div class="task-body"><button class="task-name" data-edit="'+id+'">'+name+'</button>'+
      '<div class="task-sub">'+category+' · '+t.minutes+' 分钟</div></div>'+
      '<button class="edit-task" data-edit="'+id+'" aria-label="编辑任务">⋯</button></div>';
  }
  function render(){
    $("goalLabel").textContent="目标 "+config.goal;
    $("metricDone").textContent=markCount();
    $("metricTotal").textContent="/ "+tasks.length+" 已完成";
    $("metricFill").style.width=(tasks.length?Math.round(markCount()/tasks.length*100):0)+"%";
    $("metricStreak").textContent=streakDays();
    $("taskCount").textContent="("+tasks.length+")";
    $("planSubtitle").textContent=tasks.length?("已完成 "+markCount()+" / "+tasks.length+" 项 · 为自己加油"):"今天还没有安排任务";
    const html=tasks.length?tasks.map(taskMarkup).join(""):'<div class="empty">还没有任务<br/>点击「＋ 添加」，创建第一项学习计划</div>';
    $("taskList").innerHTML=html;
    $("planList").innerHTML=html;
  }
  function tick(){
    checkDate();
    const remaining=Math.max(0,Math.floor((Date.parse(config.exam+":00+08:00")-Date.now())/1000));
    $("daysNum").textContent=remaining?Math.floor(remaining/86400):"0";
    $("hNum").textContent=pad(Math.floor(remaining/3600)%24);
    $("mNum").textContent=pad(Math.floor(remaining/60)%60);
    $("sNum").textContent=pad(remaining%60);
    const exam=new Date(config.exam+":00+08:00");
    const weekday=new Intl.DateTimeFormat("zh-CN",{timeZone:"Asia/Shanghai",weekday:"long"}).format(exam);
    $("dateLabel").textContent=config.exam.slice(0,10).replace(/-/g,".")+" · "+weekday+" · "+config.exam.slice(11);
    const now=new Date();
    $("todayText").textContent=new Intl.DateTimeFormat("zh-CN",{timeZone:"Asia/Shanghai",month:"long",day:"numeric",weekday:"long"}).format(now)+" · KEEP GOING";
  }
  function setTheme(theme){document.documentElement.dataset.theme=theme;}
  function showPage(id){
    document.querySelectorAll(".page").forEach(el=>el.classList.toggle("active",el.id===id));
    document.querySelectorAll(".nav-btn").forEach(el=>el.classList.toggle("active",el.dataset.page===id));
    if(id==="settingsPage")fillSettings();
    window.scrollTo(0,0);
  }
  function fillSettings(){
    $("scoreInput").value=config.goal;
    $("examInput").value=config.exam;
    selectedTheme=config.theme;
    renderThemes();
  }
  function renderThemes(){
    document.querySelectorAll(".theme-option").forEach(el=>el.classList.toggle("selected",el.dataset.theme===selectedTheme));
  }
  function openModal(id){
    editId=id||null;
    const task=tasks.find(t=>t.id===editId);
    $("modalTitle").textContent=task?"编辑学习任务":"新建学习任务";
    $("taskTitle").value=task?task.title:"";
    $("taskCategory").value=task?task.category:"听力";
    $("taskDuration").value=task?task.minutes:"30";
    $("deleteTask").hidden=!task;
    $("taskModal").classList.add("show");
    $("taskModal").setAttribute("aria-hidden","false");
    setTimeout(()=>$("taskTitle").focus(),90);
  }
  function closeModal(){
    $("taskModal").classList.remove("show");
    $("taskModal").setAttribute("aria-hidden","true");
    editId=null;
  }
  function commitTask(){
    const title=$("taskTitle").value.trim();
    const minutes=Number($("taskDuration").value);
    if(!title){notify("请输入任务名称");return;}
    if(!Number.isInteger(minutes)||minutes<1||minutes>600){notify("任务时长请填写 1–600 分钟");return;}
    const category=$("taskCategory").value;
    const editing=Boolean(editId);
    if(editId){
      const pos=tasks.findIndex(t=>t.id===editId);
      if(pos>=0)tasks[pos]={...tasks[pos],title,category,minutes};
    }else{
      if(tasks.length>=80){notify("最多创建 80 项任务");return;}
      const id="task_"+Date.now().toString(36)+"_"+Math.random().toString(36).slice(2,7);
      tasks.push({id,title,category,minutes});
    }
    if(save(TASKS_KEY,tasks)){
      closeModal();render();syncNative();notify(editing?"已更新任务":"任务已添加");
    }
  }
  function removeTask(){
    if(!editId)return;
    if(!window.confirm("确定删除这个任务吗？"))return;
    tasks=tasks.filter(t=>t.id!==editId);
    if(save(TASKS_KEY,tasks)){closeModal();render();syncNative();notify("任务已删除");}
  }
  function toggleTask(id){
    if(!tasks.some(t=>t.id===id))return;
    done[id]=done[id]!==true;
    if(save(DONE_PREFIX+currentDate,done)){render();syncNative();}
  }
  function commitSettings(){
    const goal=Number($("scoreInput").value);
    const exam=$("examInput").value;
    if(!Number.isInteger(goal)||goal<1||goal>710){notify("目标分数必须是 1–710 的整数");return;}
    if(!validExam(exam)){notify("请选择正确的考试日期和时间");return;}
    const previous={...config};
    config={goal,exam,theme:selectedTheme};
    if(save(CONFIG_KEY,config)){
      setTheme(config.theme);tick();render();syncNative();notify("设置已保存，桌面组件已同步");
    }else{config=previous;}
  }
  document.querySelectorAll(".nav-btn").forEach(btn=>btn.addEventListener("click",()=>showPage(btn.dataset.page)));
  $("openSettings").addEventListener("click",()=>showPage("settingsPage"));
  $("quickAdd").addEventListener("click",()=>openModal(null));
  $("planAdd").addEventListener("click",()=>openModal(null));
  $("closeModal").addEventListener("click",closeModal);
  $("taskModal").addEventListener("click",e=>{if(e.target===$("taskModal"))closeModal();});
  $("saveTask").addEventListener("click",commitTask);
  $("deleteTask").addEventListener("click",removeTask);
  $("saveSettings").addEventListener("click",commitSettings);
  document.querySelectorAll(".theme-option").forEach(btn=>btn.addEventListener("click",()=>{
    selectedTheme=btn.dataset.theme;setTheme(selectedTheme);renderThemes();
  }));
  for(const id of ["taskList","planList"]){
    $(id).addEventListener("click",e=>{
      const check=e.target.closest("[data-check]");
      if(check){toggleTask(check.dataset.check);return;}
      const edit=e.target.closest("[data-edit]");
      if(edit)openModal(edit.dataset.edit);
    });
  }
  window.addEventListener("keydown",e=>{if(e.key==="Escape")closeModal();});
  setTheme(config.theme);
  render();tick();syncNative();
  setInterval(tick,1000);
})();
