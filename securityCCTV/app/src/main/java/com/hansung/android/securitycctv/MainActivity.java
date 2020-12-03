package com.hansung.android.securitycctv;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.Toast;

import com.hansung.android.securitycctv.apicall.UpdateShadow;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

public class MainActivity extends AppCompatActivity {

    final static String TAG = "CCTV_AndroidAPI";
    WebView cctv;
    Button button;
    String state = "ON";
    String urlStr = "https://0bl6nlsm7j.execute-api.ap-northeast-2.amazonaws.com/prod/devices/MyCCTV";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        cctv = (WebView)findViewById(R.id.security_cctv);
        button = (Button)findViewById(R.id.buzzer_control);

        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(button.getText()=="Sound ON"){
                    state = "ON";
                }else if(button.getText()=="Sound OFF"){
                    state = "OFF";
                }
                JSONObject payload = new JSONObject();

                try {
                    JSONArray jsonArray = new JSONArray();

                    JSONObject tag1 = new JSONObject();
                    tag1.put("tagName", "Buzzer");
                    tag1.put("tagValue", state);

                    jsonArray.put(tag1);

                    if (jsonArray.length() > 0)
                        payload.put("tags", jsonArray);
                } catch (JSONException e) {
                    Log.e(TAG, "JSONEXception");
                }
                Log.i(TAG,"payload="+payload);
                if (payload.length() >0 ){
                    new UpdateShadow(MainActivity.this,urlStr).execute(payload);
                    if(state=="ON"){
                        button.setText("Sound OFF");
                    }else if(state=="OFF"){
                        button.setText("Sound ON");
                    }
                }
                else
                    Toast.makeText(MainActivity.this,"부저를 조작할 수 없습니다.", Toast.LENGTH_SHORT).show();
            }
        });


        WebSettings webSettings = cctv.getSettings();
        webSettings.setJavaScriptEnabled(true);

        // 화면 비율
        webSettings.setUseWideViewPort(true);       // wide viewport를 사용하도록 설정
        webSettings.setLoadWithOverviewMode(true);  // 컨텐츠가 웹뷰보다 클 경우 스크린 크기에 맞게 조정


        cctv.loadUrl("http://192.168.0.68:5000/video_feed");
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_list, menu);
        return super.onCreateOptionsMenu(menu);
    }

    @Override
    public boolean onOptionsItemSelected(@NonNull MenuItem item) {
        if (item.getItemId() == R.id.view) {
            startActivity(new Intent(this, ListActivity.class));
            return true;
        }
        return super.onOptionsItemSelected(item);
    }
}