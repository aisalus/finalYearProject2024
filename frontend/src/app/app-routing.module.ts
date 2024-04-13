import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { GenerateComponent } from './generate/generate.component';
import { UserpageComponent } from './userpage/userpage.component';
import { ResultsComponent } from './results/results.component';
import { HistoryComponent } from './history/history.component';
import { LibraryComponent } from './library/library.component';

const routes: Routes = [
  {
    path: '',
    component: GenerateComponent
  },
  {
    path: 'userpage',
    component: UserpageComponent
  },
  {
    path: 'results/:id',
    component: ResultsComponent
  },
  {
    path: 'history',
    component: HistoryComponent
  },
  {
    path: 'library',
    component: LibraryComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
