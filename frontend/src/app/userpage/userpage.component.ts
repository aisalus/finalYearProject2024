import { Component } from '@angular/core';
import { AuthService } from '@auth0/auth0-angular';
import { ApiserviceService } from '../apiservice.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-userpage',
  templateUrl: './userpage.component.html',
  styleUrl: './userpage.component.css'
})
export class UserpageComponent {
  constructor(
    public auth: AuthService,
    private api: ApiserviceService,
    private router: Router
  ) {}
  loggedIn: any = sessionStorage.getItem("loggedIn");
  user: any;
  deactivateUser(userID:any): void {
    this.api.deactivateUser(userID).subscribe(data => {
        window.location.reload();
    });
  }

  clearHistory(userID: any): void {
    userID = userID.split("|")[1];
    this.api.clearUserHistory(userID).subscribe();
  }

  clearLibrary(userID: any): void {
    userID = userID.split("|")[1];
    this.api.clearUserLibrary(userID).subscribe();
  }

  ngOnInit() {
    this.auth.user$.subscribe(data => {
      if(data == null) {
        this.router.navigateByUrl("");
      }
      else {
        this.user = data;
      }
    })
  }
}