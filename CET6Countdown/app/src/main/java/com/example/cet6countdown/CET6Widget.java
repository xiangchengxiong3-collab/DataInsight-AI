package com.example.cet6countdown;
import android.app.PendingIntent;
import android.appwidget.AppWidgetManager;
import android.appwidget.AppWidgetProvider;
import android.content.Context;
import android.content.Intent;
import android.widget.RemoteViews;
import java.time.Instant;
import java.time.Duration;
public class CET6Widget extends AppWidgetProvider {
 private static final Instant EXAM=Instant.parse("2026-12-12T07:00:00Z");
 @Override public void onUpdate(Context c,AppWidgetManager m,int[] ids){for(int id:ids)update(c,m,id);}
 private void update(Context c,AppWidgetManager m,int id){
  RemoteViews r=new RemoteViews(c.getPackageName(),R.layout.widget);
  long s=Math.max(0,Duration.between(Instant.now(),EXAM).getSeconds());
  r.setTextViewText(R.id.days,Instant.now().isBefore(EXAM)?String.valueOf(s/86400):"GO!");
  r.setTextViewText(R.id.unit,Instant.now().isBefore(EXAM)?" 天":"");
  r.setTextViewText(R.id.detail,String.format(java.util.Locale.CHINA,"%02d 小时 %02d 分钟",(s/3600)%24,(s/60)%60));
  Intent open=new Intent(c,MainActivity.class);
  PendingIntent p=PendingIntent.getActivity(c,0,open,PendingIntent.FLAG_IMMUTABLE|PendingIntent.FLAG_UPDATE_CURRENT);
  r.setOnClickPendingIntent(R.id.widget_root,p);m.updateAppWidget(id,r);
 }
}