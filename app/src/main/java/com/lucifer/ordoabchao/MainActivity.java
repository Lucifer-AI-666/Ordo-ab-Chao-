package com.lucifer.ordoabchao;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.widget.Button;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

/**
 * Minimal MainActivity:
 * - mostra titolo e pulsanti
 * - apre la pagina web integrata in assets (file:///android_asset/index.html)
 */
public class MainActivity extends AppCompatActivity {

    private WebView webView;
    private static final String WEB_URL = "file:///android_asset/index.html";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        TextView title = findViewById(R.id.titleText);
        title.setText("Ordo ab Chao - Minimal App");

        Button openBrowser = findViewById(R.id.btn_open_browser);
        openBrowser.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // Usa ACTION_VIEW su asset (device aprirà un viewer compatibile)
                Intent i = new Intent(Intent.ACTION_VIEW, Uri.parse(WEB_URL));
                startActivity(i);
            }
        });

        Button openWebView = findViewById(R.id.btn_open_webview);
        webView = findViewById(R.id.webview);
        openWebView.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                webView.setVisibility(View.VISIBLE);
                WebSettings settings = webView.getSettings();
                settings.setJavaScriptEnabled(false); // disabilitato per sicurezza
                webView.loadUrl(WEB_URL);
            }
        });
    }
}