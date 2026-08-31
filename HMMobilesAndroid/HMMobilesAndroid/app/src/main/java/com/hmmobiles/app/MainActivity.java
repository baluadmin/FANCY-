package com.hmmobiles.app;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.os.Handler;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

    private WebView webView;
    private Handler handler = new Handler();

    private boolean loggedIn = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // START IN PORTRAIT
        setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        );

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();

        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);

        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setSupportMultipleWindows(true);

        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);

        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);

        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());

        webView.loadUrl(
                "https://baluaiproject1.streamlit.app/"
        );

        // Start checking page
        checkLoginStatus();
    }

    private void checkLoginStatus() {

        handler.postDelayed(new Runnable() {

            @Override
            public void run() {

                if (webView != null) {

                    webView.evaluateJavascript(
                            "(function() {" +
                            "return document.body.innerText || '';" +
                            "})()",
                            value -> {

                                if (value == null) {
                                    return;
                                }

                                // Login page text
                                boolean loginPage =
                                        value.contains("Customer Portal Login") ||
                                        value.contains("Secure Login");

                                if (!loginPage && !loggedIn) {

                                    loggedIn = true;

                                    // CHANGE TO LANDSCAPE
                                    runOnUiThread(() -> {

                                        setRequestedOrientation(
                                                ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
                                        );

                                    });

                                } else if (loginPage && loggedIn) {

                                    loggedIn = false;

                                    // RETURN TO PORTRAIT
                                    runOnUiThread(() -> {

                                        setRequestedOrientation(
                                                ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
                                        );

                                    });
                                }
                            }
                    );
                }

                handler.postDelayed(this, 1000);
            }

        }, 4000);
    }

    @Override
    public void onBackPressed() {

        if (webView != null && webView.canGoBack()) {

            webView.goBack();

        } else {

            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {

        handler.removeCallbacksAndMessages(null);

        if (webView != null) {
            webView.destroy();
        }

        super.onDestroy();
    }
}
