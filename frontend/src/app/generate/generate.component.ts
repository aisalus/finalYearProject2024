import { Component } from '@angular/core';
import { ViewEncapsulation } from '@angular/core';
import { ApiserviceService } from '../apiservice.service';
import { NgSelectModule } from '@ng-select/ng-select';
import { AuthService } from '@auth0/auth0-angular';
import { Router } from '@angular/router';

@Component({
  selector: 'app-generate',
  templateUrl: './generate.component.html',
  styleUrl: './generate.component.css',
  encapsulation: ViewEncapsulation.None
})
export class GenerateComponent {
  constructor(
    private api: ApiserviceService,
    public ngSelect: NgSelectModule,
    public auth: AuthService,
    private router: Router
  ) {}
  selectedGameId: any;
  searchItems = [];
  userLibraryStatus = false;
  sentimentStatus = false;
  user: any;
  generateText: string = "Generate";
  loggedIn: any = sessionStorage.getItem("loggedIn");

  onSearchChange(searchValue: any): void {  
    this.api.searchGames(searchValue).subscribe(data => this.searchItems = data);
  }

  generateRec(): void {
    if(this.selectedGameId) {
      this.generateText = "Generating...";
      let userId = "";
      if (this.user != null){
        userId = this.user.sub.split('|')[1];
      }
      // Change apiCall if the user is logged in
      let apiCall = (this.user != null) ? this.api.getGameRec(this.selectedGameId, this.sentimentStatus, this.userLibraryStatus, userId) 
      : this.api.getGameRec(this.selectedGameId, this.sentimentStatus, this.userLibraryStatus);
      apiCall.subscribe(data => {
        // Add recommendation to history and send data to the results page
        this.addToHistory(data);
        this.router.navigateByUrl(`results/${data.id}`, {state: data})
      });
    }
  }

  addToHistory(data: any): void {
    if(this.user != null){
      let userId = this.user.sub.split('|')[1];
      this.api.setUserHistory(userId, data).subscribe();
    }
  }
  setLibraryStatus(val: any): void {
    this.userLibraryStatus = val.checked;
  }

  setSentimentStatus(val: any): void {
    this.sentimentStatus = val.checked;
  }

  ngOnInit() {
    this.auth.user$.subscribe(data => this.user = data);
  }
}
