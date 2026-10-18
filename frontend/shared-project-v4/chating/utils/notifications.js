// import {state} from "@/store/state";
import settings from "@/../settings";
import axios from 'axios'

function showNotification(message) {
  if (Notification.permission === "granted" && document.hidden) {
    const notification = new Notification(`إشعار جديد ${message}`, {
      body: `${message.user.first_name} ${message.user.last_name}: ${
        message.content || "رسالة وسائط"
      }`,
      icon: "@/assets/notifications.png",
    });

    notification.onclick = () => window.focus();
  }
}

function getunreadNotificationsCount(){
  var generalization_count = state.unread_generalization?.length;
  var occation_count = state.unread_occasion?.length;
  state.notifications_count = generalization_count + occation_count;
  return state.notifications_count;
};


export default function connectWebSocket() {
  const token = localStorage.getItem("token");
  const protocol = window.location.protocol === "https:" ? "wss://" : "ws://";
  const queryParam = (token && token !== "null") ? `?token=${token}` : "";
  const socketUrl = protocol + settings.websocket_url + "ws/notifications/?token=" + queryParam;

  const websocket = new WebSocket(socketUrl);

  websocket.onopen = () => {
  };

  websocket.onmessage = async (event) => {
    const data = JSON.parse(event.data);

    if (data.notification_type == 1) {
      try {
        const response = await axios.get(
          "system-management/generalizations-notifications",
          {
            params: {
              user: state.profile?.id,
            },
          }
        );
        state.unread_generalization = response.data;
      } catch (error) {
        console.error("Error fetching group generalizations:", error);
      }
    }else if(data.notification_type == 2) {
      try {
        // const response = await axios.get(
        //   "system-management/regulations-notifications",
        //   {
        //     params: {
        //       user: state.profile?.id,
        //     },
        //   }
        // );
        state.unread_regulations = [];
      } catch (error) {
        console.error("Error fetching group regulations:", error);
      }
    }
  };

  websocket.onclose = () => {
    // console.log("WebSocket connection closed for notifications");
  };

  return websocket;
}
