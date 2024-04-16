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
  submitText: string = "Submit";

  deactivateUser(userID:any): void {
    this.api.deactivateUser(userID).subscribe(data => {
      sessionStorage.removeItem("loggedIn");
      this.auth.logout();
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

  addSuggestion(message: string): void {
    if(message != ""){
      let data = {"suggestionMessage":message};
      console.log(data);
      this.api.addSuggestion(data).subscribe();
      this.submitText = "Submitted!";
    }
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