package com.example.cet6countdown;

import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.widget.RemoteViews;
import android.graphics.Color;
import java.time.Duration;
import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Locale;

public class CET6Widget extends AppWidgetProvider {
    private static final ZoneId BEIJING=ZoneId.of("Asia/Shanghai");
    private static final DateTimeFormatter FORM=DateTimeFormatter.ofPattern("yyyy.MM.dd HH:mm",Locale.CHINA);

    @Override
    public void onUpdate(Context ctx, AppWidgetManager manager, int[] ids) {
        for(int id:ids) update(ctx,manager,id);
    }

    public static void updateAll(Context ctx){
        AppWidgetManager manager=AppWidgetManager.getInstance(ctx);
        int[] ids=manager.getAppWidgetIds(new ComponentName(ctx,CET6Widget.class));
        for(int id:ids)update(ctx,manager,id);
    }

    private static void update(Context ctx,AppWidgetManager manager,int id){
        SharedPreferences sp=ctx.getSharedPreferences("cet6_widget",Context.MODE_PRIVATE);
        String examText=sp.getString("exam","2026-12-12T15:00");
        int goal=sp.getInt("goal",550);
        int total=sp.getInt("total",4);
        int completed=sp.getInt("completed",0);
        String today=java.time.LocalDate.now(BEIJING).toString();
        if(!today.equals(sp.getString("progressDate",""))) completed=0;
        String theme=sp.getString("theme","midnight");
        LocalDateTime local;
        try {local=LocalDateTime.parse(examText);}
        catch(Exception ex) {local=LocalDateTime.of(2026,12,12,15,0);}
        Instant exam=local.atZone(BEIJING).toInstant();
        long seconds=Math.max(0,Duration.between(Instant.now(),exam).getSeconds());
        long days=seconds/86400;
        RemoteViews view=new RemoteViews(ctx.getPackageName(),R.layout.widget);
        boolean light="light".equals(theme), violet="violet".equals(theme);
        if(light)view.setInt(R.id.widget_root,"setBackgroundResource",R.drawable.background_light);
        else if(violet)view.setInt(R.id.widget_root,"setBackgroundResource",R.drawable.background_violet);
        else view.setInt(R.id.widget_root,"setBackgroundResource",R.drawable.background);
        int headline=light?Color.rgb(27,54,47):Color.rgb(232,255,248);
        int muted=light?Color.rgb(80,107,95):Color.rgb(173,205,209);
        int accent=light?Color.rgb(20,122,101):violet?Color.rgb(210,183,255):Color.rgb(130,231,209);
        view.setTextColor(R.id.w_tag,accent);
        view.setTextColor(R.id.w_goal,accent);
        view.setTextColor(R.id.days,headline);
        view.setTextColor(R.id.unit,accent);
        view.setTextColor(R.id.detail,muted);
        view.setTextColor(R.id.w_date,muted);
        view.setTextColor(R.id.w_progress,muted);
        view.setTextViewText(R.id.w_tag,"CET-6  ·  COUNTDOWN");
        view.setTextViewText(R.id.w_goal,"GOAL "+goal);
        view.setTextViewText(R.id.days,days+"");
        view.setTextViewText(R.id.unit,"天");
        view.setTextViewText(R.id.detail,
                String.format(Locale.CHINA,"%02d小时  %02d分钟",(seconds/3600)%24,(seconds/60)%60));
        view.setTextViewText(R.id.w_date,FORM.format(local)+" 北京时间");
        view.setTextViewText(R.id.w_progress,"今日完成  "+completed+" / "+total);
        view.setProgressBar(R.id.widget_progress,Math.max(1,total),Math.min(Math.max(0,completed),Math.max(1,total)),false);
        Intent intent=new Intent(ctx,MainActivity.class);
        PendingIntent pending=PendingIntent.getActivity(ctx,0,intent,
            PendingIntent.FLAG_IMMUTABLE|PendingIntent.FLAG_UPDATE_CURRENT);
        view.setOnClickPendingIntent(R.id.widget_root,pending);
        manager.updateAppWidget(id,view);
    }
}
