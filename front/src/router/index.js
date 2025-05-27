import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import SignupView from '@/views/SignupView.vue'
import LoginView from '@/views/LoginView.vue'
import MyPageView from '@/views/MypageView.vue'
import ProductView from '@/views/ProductView.vue'
import WeddingCalculatorView from '@/views/WeddingCalculatorView.vue'
import RingView from '@/views/RingView.vue'
import BoardView from '@/views/BoardView.vue'
import SearchView from '@/views/SearchView.vue'
// import DepositDetailView from '@/views/DepositDetailView.vue'  
// import SavingDetailView from '@/views/SavingDetailView.vue'
import ArticleCreateView from '@/views/ArticleCreateView.vue'
import ArticleDetailView from '@/views/ArticleDetailView.vue'
import LoanView from '@/views/LoanView.vue'
import VideoDetailView from '@/views/VideoDetailView.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: MainView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignupView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/mypage',
      name: 'mypage',
      component: MyPageView
    },
    {
      path: '/products',
      name: 'products',
      component: ProductView
    },
    {
      path: '/calculator',
      name: 'calculator',
      component: WeddingCalculatorView
    },
    {
      path: '/weddingring',
      name: 'weddingring',
      component: RingView
    },
    {
      path: '/board',
      name: 'board',
      component: BoardView
    },
    {
      path: '/search',
      name: 'search',
      component: SearchView,
    },
    // {
    //   path: '/products/deposits/:deposit_code/options/:option_id',
    //   name: 'DepositDetail',
    //   component: DepositDetailView
    // },
    // {
    //   path: '/products/savings/:saving_code/options/:option_id',
    //   name: 'SavingDetail',
    //   component: SavingDetailView
    // },
    {
    path: '/board/create',
    name: 'board-create',
    component: ArticleCreateView
  },
  {
    path: '/board/:id',
    name: 'board-detail',
    component: ArticleDetailView
  },   
  {
    path: '/loans',
    name: 'loan-list',
    component: LoanView
  }, 
  {
  path: '/video/:id',
  name: 'videoDetail',
  component: VideoDetailView
  }, 
  ],
})

export default router
