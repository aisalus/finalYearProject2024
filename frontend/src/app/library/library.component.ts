import { Component } from '@angular/core';
import { ApiserviceService } from '../apiservice.service';

@Component({
  selector: 'app-library',
  templateUrl: './library.component.html',
  styleUrl: './library.component.css'
})
export class LibraryComponent {
  constructor (
    private api: ApiserviceService
  ) {}

  items: any[] = [];
  id: any = "";
  selectedGameId: any;
  searchItems = [];

  onSearchChange(searchValue: any): void {  
    this.api.searchGames(searchValue).subscribe(data => this.searchItems = data);
  }

  addToLibrary(): void {
    let data = {"gameId":this.selectedGameId}
    this.api.setUserLibrary(this.id, data).subscribe(data => window.location.reload());
  }

  deleteItem(id: string, lid: string): void {
    this.api.deleteFromLibrary(id, lid).subscribe(data => window.location.reload());
  }

  ngOnInit() {
    this.id = sessionStorage.getItem("userId");
    this.api.getUserLibrary(this.id).subscribe(data => {this.items = data;});
  }
}
