package com.example.paloslanesapp;

import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import android.text.TextWatcher;
import android.view.View;

import androidx.core.view.GravityCompat;
import androidx.appcompat.app.ActionBarDrawerToggle;

import android.view.MenuItem;

import com.google.android.material.navigation.NavigationView;

import androidx.drawerlayout.widget.DrawerLayout;

import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.widget.Toolbar;
import androidx.fragment.app.FragmentTransaction;

import android.view.Menu;
import android.widget.CheckBox;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        NavigationView navigationView = findViewById(R.id.nav_view);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.addDrawerListener(toggle);
        toggle.syncState();
        navigationView.setNavigationItemSelectedListener(this);

    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main_menu, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        if (id == R.id.menu_Login) {
            Intent login = new Intent(this,LoginPage.class);
            startActivity(login);
        }
        else if (id == R.id.menu_Logout) {
            Intent logout = new Intent(this,LoginPage.class);
            startActivity(logout);
        }
        return super.onOptionsItemSelected(item);
    }

        @Override
    public void onBackPressed() {
        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        //Create a transaction

        FragmentTransaction transaction = getSupportFragmentManager().beginTransaction();
        int id = item.getItemId();

        if (id == R.id.nav_home) {
            Intent home = new Intent(this,MainActivity.class);
            startActivity(home);
        } else if (id == R.id.nav_coupons) {
            Coupons fragment = new Coupons();
            transaction.replace(R.id.fragmentHolder, fragment);
        } else if (id == R.id.nav_LeagueStandings) {
            startActivity((new Intent(Intent.ACTION_VIEW, Uri.parse("http://www.paloslanes.net/leaguestandings1.htm"))));
        } else if (id == R.id.nav_LeagueSignUp) {
            startActivity((new Intent(Intent.ACTION_VIEW, Uri.parse("http://www.paloslanes.net/leagues1.htm"))));
        } else if (id == R.id.nav_Loyalty) {
            Loyalty fragment = new Loyalty();
            transaction.replace(R.id.fragmentHolder, fragment);
        } else if (id == R.id.nav_PartyPackages) {
            Party fragment = new Party();
            transaction.replace(R.id.fragmentHolder, fragment);
        }

        transaction.addToBackStack(null);

        transaction.commit();

        DrawerLayout drawer = findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);
        return true;
    }
}
