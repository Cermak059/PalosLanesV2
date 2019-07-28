package com.example.paloslanesapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;

public class SignUpPage extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up_page);
    }

    public void btnSubmit (View view) {
        Intent home = new Intent(this,MainActivity.class);
        startActivity(home);
    }
}
