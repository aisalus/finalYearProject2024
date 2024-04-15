import { Component } from '@angular/core';
import { ApiserviceService } from '../apiservice.service';

@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrl: './history.component.css'
})
export class HistoryComponent {
  constructor (
    private api: ApiserviceService
  ) {}
  items: any[] = [];
  id: any = "";

  ngOnInit() {
    this.id = sessionStorage.getItem("userId");
    this.api.getUserHistory(this.id).subscribe(data => {this.items = data;});
  }
}
