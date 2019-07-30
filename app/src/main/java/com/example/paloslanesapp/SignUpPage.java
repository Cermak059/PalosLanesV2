package com.example.paloslanesapp;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.telecom.Call;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;


public class SignUpPage extends AppCompatActivity {

    EditText bDay;
    EditText fname;
    EditText lname;
    EditText email;
    EditText phone;
    EditText newUser;
    EditText newPass;
    EditText confirm;
    Button submit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_sign_up_page);

        //Create references to UI
        final EditText fname = (EditText) findViewById(R.id.editFname);
        final EditText lname = (EditText) findViewById(R.id.editLname);
        final EditText email = (EditText) findViewById(R.id.editEmail);
        final EditText phone = (EditText) findViewById(R.id.editPhone);
        final EditText bDay = (EditText) findViewById(R.id.editBirthDate);
        Button submit = (Button) findViewById(R.id.btnSubmit);

        //Create onClickListener for button submit
        submit.setOnClickListener(new View.OnClickListener() {
            @Override
            //Validate text when submit button is clicked
            public void onClick(View view) {
                final String FirstName = fname.getText().toString();
                final String LastName = lname.getText().toString();
                final String Email = email.getText().toString();
                final String Phone = phone.getText().toString();
                final String Birthday = bDay.getText().toString();
                //validate first name text
                if (FirstName.length()==0) {
                    fname.requestFocus();
                    fname.setError("Field cannot be empty");
                }
                else if (FirstName.length()==1) {
                    fname.requestFocus();
                    fname.setError("Must be atleast 2 characters");
                }
                else if (!FirstName.matches("[a-zA-Z]+")) {
                    fname.requestFocus();
                    fname.setError("Use only alphabetical characters");
                }
                //validate last name text
                else if (LastName.length()==0) {
                    lname.requestFocus();
                    lname.setError("Field cannot be empty");
                }
                else if (LastName.length()==1) {
                    lname.requestFocus();
                    lname.setError("Must be atleast 2 characters");
                }
                else if (!LastName.matches("[a-zA-Z]+")) {
                    lname.requestFocus();
                    lname.setError("Use only alphabetical characters");
                }
                else if (Birthday.length()==12) {
                    bDay.requestFocus();
                    bDay.setError("Must us the format 00/00/0000");
                }
                else if (!Birthday.matches("[0-9/]+")) {
                    bDay.requestFocus();
                    bDay.setError("Use only numerical characters");
                }
                else if (Email.length()==0) {
                    email.requestFocus();
                    email.setError("Field cannot be empty");
                }
                else if (Phone.length()!=12) {
                    phone.requestFocus();
                    phone.setError("Must use format 123-123-1234");
                }
                else if (!Phone.matches("[0-9-]+")) {
                    phone.requestFocus();
                    phone.setError("Use only numerical values");
                }
                else {
                    Toast.makeText(SignUpPage.this,"Thank you for signing up",Toast.LENGTH_LONG).show();
                    New();
                }
            }
        });
    }
    public void New() {
        Intent homepage = new Intent(this,MainActivity.class);
        startActivity(homepage);
    }

}
