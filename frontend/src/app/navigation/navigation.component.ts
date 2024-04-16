import { Component } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { ApiserviceService } from '../apiservice.service'
import { Router } from '@angular/router';

@Component({
  selector: 'app-navigation',
  templateUrl: './navigation.component.html'
})
export class NavigationComponent {
  constructor(
    public auth: AuthService,
    private api: ApiserviceService,
    private router: Router
  ) {}
  user: any;
  loggedIn: any = sessionStorage.getItem("loggedIn");

  // Send user data to the api
  setUserData(user: any){
    if(user != null){
      let id = user['sub'].split('|')[1];
      sessionStorage.setItem("userId", id);
      let userData = {
        "user_id": id,
        "name": user['name']
      }
      this.api.addUser(userData).subscribe();
    }
  }

  logOut(): void {
    sessionStorage.removeItem("loggedIn");
    sessionStorage.removeItem("userId");
    this.auth.logout();
    window.location.reload();
  }

  ngOnInit() {
    this.auth.user$.subscribe(data => this.setUserData(data));
    this.auth.isAuthenticated$.subscribe(data => {
      if(data && this.loggedIn == null){
        sessionStorage.setItem("loggedIn", "true");
        window.location.reload();
      }
    });
  }
}