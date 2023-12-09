import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HistoryDetailComponent } from './history-detail/history-detail.component';
import { MainComponent } from './main-page/main.component';

const routes: Routes = [
  { path: '', component: MainComponent },
  { path: 'history/:id', component: HistoryDetailComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
