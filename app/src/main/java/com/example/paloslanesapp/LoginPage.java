package com.example.paloslanesapp;

import androidx.appcompat.app.AppCompatActivity;


import android.widget.Toast;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

public class LoginPage extends AppCompatActivity {

    EditText User;
    EditText Pass;
    Button Login;
    CheckBox Remember;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login_page);

        final EditText User = (EditText) findViewById(R.id.editUserName);
        final EditText Pass = (EditText) findViewById(R.id.editPassword);
        Button Login = (Button) findViewById(R.id.btnLogin);
        CheckBox Remember = (CheckBox) findViewById(R.id.checkBoxRemember);
        Login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                final String Username = User.getText().toString();
                final String Password = Pass.getText().toString();
            if (Username.length()==0) {
                User.requestFocus();
                User.setError("Field cannot be empty");
            }
            else  if(!Username.matches("[a-zA-Z]+")) {
                User.requestFocus();
                User.setError("Use only Alpabetical characters");
            }
            else if (Password.length()==0) {
                Pass.requestFocus();
                Pass.setError("Field cannot be empty");
            }
            else {
                Toast.makeText(LoginPage.this,"Authentication Successful",Toast.LENGTH_LONG).show();
                New();
            }

            }
        });
    }

    public void New() {
        Intent homepage = new Intent(this,MainActivity.class);
        startActivity(homepage);
    }

    public void btnClick (View view) {
        Intent signup = new Intent(this,SignUpPage.class);
        startActivity(signup);
    }

}
