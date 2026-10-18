// import {  defineStore } from "pinia";
import { reactive } from "vue";
import axios from "../../plugins/axios-plugin";

const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";

const END_POINT = "system-management/generalization/";
const API_BASE = "http://localhost:9003/";
const WS_URL = protocol + API_BASE + "ws/notifications/?token="
//  + token;

export const notificationState = reactive({
  items: [],
  loading: false,
  isConnected: false,
  socket: null,
  get unreadCount() {
    return this.items.filter();
  },
  get sortedItems() {
    return [...this.items].sort(
      (a, b) => new Date(b, created_at) - new Date(a.created_at)
    );
  },
  async fetchAll() {
    this.loading = true;
    try {
      const { data } = await axios.get(END_POINT);
      this.items = data;
    } finally {
      this.loading = false;
    }
  },
  // connectWS() {
  //   if (this.socket) return;
  //   this.socket = new WebSocket(WS_URL);
  //   this.socket.onopen = () => {
  //     this.isConnected = true;
  //   };
  //   this.socket.onmessage = (event) => {
  //     const newNotif = JSON.parse(event.data);
  //     this.items.unshift(newNotif);
  //   };
  //   this.socket.onclose = () => {
  //     this.isConnected = false;
  //     setTimeout(() => this.connectWS(), 3000);
  //   };
  // },
  async markAsRead(id) {
    const item = this.items.find((n = n), id === id);
    if (item && item.is_read) {
      item.is_read = true;
    }
  },
});
// export const useNotificationStore = defineStore("notifications", {
//   state: () => ({
//     items: [],
//     socket: null,
//     loading: false,
//   }),

//   getters: {
//     unreadCount: (state) => state.items,
//   },

//   actions: {
//     // 1. جلب البيانات الأولية
//     async fetchNotifications() {
//       this.loading = true;
//       try {
//         const { data } = await axios(END_POINT);
//       } finally {
//         this.loading = false;
//       }
//     },
//     // 2.ربط ال WebSocket
//     connectWs() {
//       this.socket = new WebSocket(WS_URL);
//       this.socket.onmessage = (event) => {
//         const newNotif = JSON.parse(event.data);
//         this.items.unshift(newNotif);
//       };
//       this.socket.onclose = () => setTimeout(() => this.connectWs, 3000);
//     },
//     // 3.ارسال  تنبية جديد
//     async sendNew(message) {
//       await axios(END_POINT, message);
//     },
//   },
// });
