package com.hmmobiles.app;

import android.app.Activity;
import android.content.pm.ActivityInfo;
import android.os.Bundle;
import android.os.Handler;
import android.webkit.JavascriptInterface;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

    private WebView webView;
    private Handler handler = new Handler();

    private boolean landscapeMode = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // App starts in PORTRAIT
        setRequestedOrientation(
                ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
        );

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();

        // Streamlit requires JavaScript
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);

        settings.setJavaScriptCanOpenWindowsAutomatically(true);
        settings.setSupportMultipleWindows(true);

        // Desktop-style website
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);

        // Zoom
        settings.setSupportZoom(true);
        settings.setBuiltInZoomControls(true);
        settings.setDisplayZoomControls(false);

        // Keep website inside the app
        webView.setWebViewClient(new WebViewClient());
        webView.setWebChromeClient(new WebChromeClient());

        // Android JavaScript bridge
        webView.addJavascriptInterface(
                new AndroidBridge(),
                "AndroidBridge"
        );

        // Load HM Mobiles
        webView.loadUrl(
                "https://baluaiproject1.streamlit.app/"
        );

        // Start monitoring Streamlit buttons
        startButtonMonitor();
    }


    // ============================================================
    // MONITOR STREAMLIT BUTTONS
    // ============================================================

    private void startButtonMonitor() {

        handler.postDelayed(new Runnable() {

            @Override
            public void run() {

                if (webView != null) {

                    String javascript =
                            "(function() {" +

                            "var buttons = document.querySelectorAll('button');" +

                            "for (var i = 0; i < buttons.length; i++) {" +

                            "var text = (buttons[i].innerText || " +
                            "buttons[i].textContent || '').trim();" +

                            // LOGIN BUTTON
                            "if (text === 'Secure Login' && " +
                            "!buttons[i].dataset.androidLoginHooked) {" +

                            "buttons[i].dataset.androidLoginHooked = 'true';" +

                            "buttons[i].addEventListener('click', function() {" +

                            "if (window.AndroidBridge) {" +
                            "window.AndroidBridge.loginClicked();" +
                            "}" +

                            "});" +

                            "}" +

                            // LOGOUT BUTTON
                            "if (text === 'Logout' && " +
                            "!buttons[i].dataset.androidLogoutHooked) {" +

                            "buttons[i].dataset.androidLogoutHooked = 'true';" +

                            "buttons[i].addEventListener('click', function() {" +

                            "if (window.AndroidBridge) {" +
                            "window.AndroidBridge.logoutClicked();" +
                            "}" +

                            "});" +

                            "}" +

                            "}" +

                            "})();";

                    webView.evaluateJavascript(
                            javascript,
                            null
                    );
                }

                // Check every 500 milliseconds
                handler.postDelayed(this, 500);
            }

        }, 2000);
    }


    // ============================================================
    // ANDROID BRIDGE
    // ============================================================

    public class AndroidBridge {

        @JavascriptInterface
        public void loginClicked() {

            runOnUiThread(new Runnable() {

                @Override
                public void run() {

                    if (!landscapeMode) {

                        landscapeMode = true;

                        // CHANGE TO LANDSCAPE
                        setRequestedOrientation(
                                ActivityInfo.SCREEN_ORIENTATION_LANDSCAPE
                        );
                    }
                }
            });
        }


        @JavascriptInterface
        public void logoutClicked() {

            runOnUiThread(new Runnable() {

                @Override
                public void run() {

                    if (landscapeMode) {

                        landscapeMode = false;

                        // RETURN TO PORTRAIT
                        setRequestedOrientation(
                                ActivityInfo.SCREEN_ORIENTATION_PORTRAIT
                        );
                    }
                }
            });
        }
    }


    // ============================================================
    // BACK BUTTON
    // ============================================================

    @Override
    public void onBackPressed() {

        if (webView != null && webView.canGoBack()) {

            webView.goBack();

        } else {

            super.onBackPressed();
        }
    }


    // ============================================================
    // CLEANUP
    // ============================================================

    @Override
    protected void onDestroy() {

        handler.removeCallbacksAndMessages(null);

        if (webView != null) {
            webView.destroy();
        }

        super.onDestroy();
    }
}
