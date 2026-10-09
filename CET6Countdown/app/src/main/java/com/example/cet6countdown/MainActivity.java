package com.example.cet6countdown;

import android.app.Activity;
import android.content.ComponentName;
import android.content.SharedPreferences;
import android.appwidget.AppWidgetManager;
import android.graphics.Color;
import android.os.Bundle;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;

public class MainActivity extends Activity {
    private WebView webView;

    @Override
    public void onCreate(Bundle state) {
        super.onCreate(state);
        getWindow().setStatusBarColor(Color.rgb(11,17,30));
        getWindow().setNavigationBarColor(Color.rgb(11,17,30));
        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(11,17,30));
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.getSettings().setAllowFileAccess(false);
        webView.getSettings().setAllowContentAccess(false);
        webView.addJavascriptInterface(new SettingsBridge(), "CETBridge");
        webView.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return !url.startsWith("https://cet6.local/");
            }
        });
        setContentView(webView);
        try {
            String html = readAsset("index.html")
                .replace("/*__CSS__*/", readAsset("style.css"))
                .replace("/*__JS__*/", readAsset("app.js"));
            // Retain the previous application's origin for localStorage migration.
            webView.loadDataWithBaseURL("https://cet6.local/",html,"text/html","UTF-8",null);
        } catch(Exception error) {
            webView.loadDataWithBaseURL("https://cet6.local/",
                "<h2 style='color:white'>页面加载失败，请重新安装。</h2>","text/html","UTF-8",null);
        }
    }

    private String readAsset(String filename) throws Exception {
        StringBuilder out = new StringBuilder();
        BufferedReader reader = new BufferedReader(new InputStreamReader(
            getAssets().open(filename), StandardCharsets.UTF_8));
        try {
            String line;
            while((line=reader.readLine())!=null) out.append(line).append('\n');
        } finally { reader.close(); }
        return out.toString();
    }

    private class SettingsBridge {
        @JavascriptInterface
        public void syncWidget(String exam, String goal, int completed, int total, String theme) {
            if(exam==null||!exam.matches("\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}")) return;
            int score;
            try { score=Integer.parseInt(goal); }
            catch(Exception e) { return; }
            if(score<1||score>710) return;
            if(!"violet".equals(theme)&&!"light".equals(theme)) theme="midnight";
            final String activeTheme=theme;
            SharedPreferences prefs=getSharedPreferences("cet6_widget",MODE_PRIVATE);
            prefs.edit().putString("exam",exam).putInt("goal",score)
                .putInt("completed",Math.max(0,completed))
                .putInt("total",Math.max(0,total))
                .putString("theme",activeTheme).apply();
            runOnUiThread(() -> {
                int barColor;
                if("light".equals(activeTheme)) barColor=Color.rgb(247,247,241);
                else if("violet".equals(activeTheme)) barColor=Color.rgb(17,16,32);
                else barColor=Color.rgb(11,17,30);
                getWindow().setStatusBarColor(barColor);
                getWindow().setNavigationBarColor(barColor);
                getWindow().getDecorView().setSystemUiVisibility("light".equals(activeTheme)
                    ? (android.view.View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | android.view.View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR) : 0);
                CET6Widget.updateAll(MainActivity.this);
            });
        }
    }

    @Override
    protected void onDestroy() {
        if(webView!=null){ webView.destroy();webView=null; }
        super.onDestroy();
    }
}
