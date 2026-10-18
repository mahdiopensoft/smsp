// added by samer
 

import "./styles/style.css";

/* 1. Base / Reset */
import './styles/base/reset.css';
import './styles/base/typography.css';
// * 2. Design Tokens */
import './styles/tokens/colors.css';
import './styles/tokens/spacing.css';
import './styles/tokens/radius.css';
import './styles/tokens/shadows.css';
import './styles/tokens/motion.css';
// * 3. Components */
import './styles/components/buttons.css';
import './styles/components/sidebar.css';
import './styles/components/navbar.css';
import './styles/components/filter.css';
import './styles/components/layout.css';
import './styles/components/datatable.css';


const components = import.meta.glob("./components/**/*.vue");
import CustomRouter from "./src/components/CustomRouter.vue";
import Home from "./src/Home.vue";
import SideBar from "./src/layouts/SideBar.vue";
import { HandelError } from "./src/utils/HandelError";
import ValueValidationPlugin from "./src/utils/validation";
import Globals from "./src/utils/Globals";
import api from "./plugins/axios-plugin.js";
import {
  controlRoutes,
  checkAuth,
  convertToObject,
  convertFromObject,
  ExportToExcel,
  printReport,
  getData,
  logOut,
  alert,
  showAlert,
  changeKeyScreen,
  showSnackBar,
} from "./src/utils/Globals";

import AllowDataEntery from "./components/other/ImportExcel/AllowDataEntery.vue";
import ScreenView from "./src/page/ScreenManagement/ScreenView.vue";
import dynamicRoutes from "./src/utils/Route";

import InitializationView from "./src/page/InitializationScreen/InitializationView.vue";
import AddInitialization from "./src/page/InitializationScreen/AddInitialization.vue";

import OrganizationTree from "./src/page/Organization/OrganizationTree.vue";
import OrganizationScreen from "./src/page/Organization/OrganizationScreen.vue";
import OrganizationBasicData from "./src/page//Organization/OrganizationBasicData/OrganizationBasicData.vue";

import InstructionsView from "./src/page/Instructions/InstructionsView.vue";
import useNavigateTo from "./src/composables/useNavigateTo";
import Alert from "./components/dialog/Alert/Alert.vue";

import LogIn from "./src/UserManagement/views/auth/LoginPage.vue";
import SSOLoginPage from "./src/UserManagement/views/auth/SSOLoginPage.vue";
import SSOCallback from "./src/UserManagement/views/auth/SSOCallback.vue";
import LogoutSuccess from "./src/UserManagement/views/auth/LogoutSuccess.vue";
import AuthCallback from "./src/UserManagement/views/auth/AuthCallback.vue";
import AuthError from "./src/UserManagement/views/auth/AuthError.vue";
import SystemSelector from "./src/UserManagement/views/SystemSelector.vue";
import dashboardSSo from "./src/UserManagement/views/DashboardSSo.vue";
import UsersPage from "./src/UserManagement/views/admin/Users/UserView.vue";
import SyncPage from "./src/UserManagement/views/admin/SyncPage.vue";
import UserTypesPage from "./src/UserManagement/views/admin/UserType/TypeUserView.vue";
import GroupsPage from "./src/UserManagement/views/admin/Groups/GroupsUserView.vue";

import CountryView from "./src/UserManagement/Country/CountryView.vue";
import GovernorateView from "./src/UserManagement/Country/Children/Governorate/GovernorateView.vue";
import ProfilePage from "./src/UserManagement/views/profile/ProfilePage.vue";
import { useAuthStore } from "./src/UserManagement/stores/auth";
import routers from "./src/router";
import { primaryStore } from "./store/state";

// Security components
import MFAVerifyStep from "./src/UserManagement/views/auth/MFAVerifyStep.vue";

import App from "./src/App.vue";

import ar from "./src/locales/ar.json";
import en from "./src/locales/en.json";

import { useCustomHeaderFooter } from "./src/headerandfooter/composables/useCustomHeaderFooter";
import vAuth from "./src/directives/auth"
import SystemInfo from "./src/page/SystemInfo.vue"

function isSSO() {
  const auth = useAuthStore();

  return auth.isSSO;
}

const shared = {


  api,
  //  components
  components,
  Alert,
  CustomRouter,

  //  page
  Home,

  SideBar,
  ScreenView,

  // log in
  routers,
  useAuthStore,
  LogIn,
  SSOLoginPage,
  SSOCallback,
  AuthCallback,
  AuthError,
  LogoutSuccess,
  SystemSelector,
  dashboardSSo,
  UsersPage,
  SyncPage,
  UserTypesPage,
  GroupsPage,
  CountryView,
  GovernorateView,
  ProfilePage,

  AllowDataEntery,
  InitializationView,
  AddInitialization,

  OrganizationTree,
  OrganizationScreen,
  OrganizationBasicData,
  InstructionsView,

  //  functions
  alert,
  showAlert,
  showSnackBar,
  changeKeyScreen,
  HandelError,
  controlRoutes,
  Globals,
  ValueValidationPlugin,
  checkAuth,
  dynamicRoutes,
  convertToObject,
  ExportToExcel,
  convertFromObject,
  printReport,
  getData,
  logOut,

  useNavigateTo,

  addedRotes: primaryStore.addedRoutes,

  // Security
  MFAVerifyStep,

  App,
  isSSO,
  ar,
  en,

  SSOMode: SSOMode,
  useHeaderFooter:useCustomHeaderFooter,
  vAuth,

  SystemInfo
};


function SSOMode(mode = "keycloak") {
  return localStorage.getItem("authMode") == mode;
}
export default shared;
