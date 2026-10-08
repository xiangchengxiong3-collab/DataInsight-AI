package com.example.cet6countdown;
import android.app.Activity;
import android.os.Bundle;
import android.graphics.Color;
import android.webkit.WebView;
import android.webkit.WebViewClient;
public class MainActivity extends Activity {
  private WebView view;
  @Override public void onCreate(Bundle b) { super.onCreate(b);
    getWindow().setStatusBarColor(Color.rgb(9,13,24)); getWindow().setNavigationBarColor(Color.rgb(9,13,24));
    view = new WebView(this); view.setBackgroundColor(Color.rgb(9,13,24)); view.getSettings().setJavaScriptEnabled(true); view.getSettings().setDomStorageEnabled(true);
    view.setWebViewClient(new WebViewClient()); setContentView(view);
    view.loadDataWithBaseURL("https://cet6.local/",HTML,"text/html","UTF-8",null);
  }
  @Override protected void onDestroy(){ if(view!=null){view.destroy();view=null;} super.onDestroy(); }
  private static final String HTML = "<!doctype html><html lang='zh-CN'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>六级倒计时</title><style>body{margin:0;padding:32px 24px;box-sizing:border-box;background:linear-gradient(150deg,#193348,#090d18 65%);color:#e6fff9;font-family:sans-serif;min-height:100vh}small{color:#91c9c3}h1{margin-top:55px;font-size:25px}#days{font-size:108px;letter-spacing:-5px;font-weight:800}section{border:1px solid #325760;background:#142a3b;padding:20px;border-radius:24px;margin:25px 0}label{display:block;margin:19px 0}input{accent-color:#8ce2c9}p{color:#bdd4de;font-size:14px}</style></head><body><small>CET-6 · GOAL 550</small><h1>距离英语六级考试</h1><section><small>距离考试还有</small><div><span id='days'>--</span> 天</div><p id='detail'>-- 小时 -- 分钟 -- 秒</p><p>2026.12.12 周六 15:00 北京时间</p></section><h3>今日复习计划</h3><label><input type='checkbox' data-id='listening'> 听力 30 分钟</label><label><input type='checkbox' data-id='reading'> 阅读 25 分钟</label><label><input type='checkbox' data-id='words'> 词汇 20 分钟</label><label><input type='checkbox' data-id='writing'> 写作或翻译 15 分钟</label><script>const end=Date.parse('2026-12-12T15:00:00+08:00');function tick(){let n=Math.max(0,Math.floor((end-Date.now())/1000));document.getElementById('days').textContent=Math.floor(n/86400);let p=v=>String(v).padStart(2,'0');document.getElementById('detail').textContent=p(Math.floor(n/3600)%24)+' 小时 '+p(Math.floor(n/60)%60)+' 分钟 '+p(n%60)+' 秒';}tick();setInterval(tick,1000);let today=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());document.querySelectorAll('input').forEach(e=>{let k='c6-'+today+'-'+e.dataset.id;try{e.checked=localStorage.getItem(k)==='1'}catch(x){}e.onchange=()=>{try{localStorage.setItem(k,e.checked?'1':'0')}catch(x){}}});</scr"+"ipt></body></html>";
}