package com.example.paloslanesapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class LoginPage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login_page);
    }

    public void btnLogin (View view) {
        Intent main = new Intent(this, MainActivity.class);
        startActivity(main);
    }

    public void btnClick (View view) {
        Intent signup = new Intent(this,SignUpPage.class);
        startActivity(signup);
    }

}
