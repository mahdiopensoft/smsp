<template>
  <!-- added by samer -->
  <!-- سجل العمليات -->
  <custom-data-table
    v-model="selectedItem"
    :="{
      headers,
      items,
      getData,
      customTable: false,
      actions: false,
      log: false,
     
    }"
  >
    <template v-slot:item="{ item, index }">
      <tr>
        <td class="print">
          <v-checkbox-btn
            v-model="selectedItem"
            :value="item"
            :key="item.id"
            hide-details
            density
            class="ms-1"
          />
        </td>
        <td>{{index+1}}</td>
        
        <td>{{ item.user_name_ar ?? "" }}</td>
        <td>{{ item.action.ar ?? "" }}</td>
        <td>{{ item.viewset.ar ?? "" }}</td>
        <td>{{ item.created_at ?? "" }}</td>
        <td>{{ item.client_info.ip ?? "" }}</td>
        <td>{{ item.client_info.device.os ?? "" }}</td>
        <td>{{ item.client_info.device.is_pc ?? "" }}</td>
        <td>{{ item.client_info.device.device ?? "" }}</td>
        <td>{{ item.client_info.device.browser ?? "" }}</td>
        <td>{{ item.client_info.device.is_mobile ?? "" }}</td>
        <td>{{ item.client_info.device.is_tablet ?? "" }}</td>
        <td>{{ item.client_info.device.is_touch_capable ?? "" }}</td>
      </tr>
    </template>
  </custom-data-table>
</template>
<script>
export default {
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "log/action-logs/",

      selectedItem: [],
    };
  },
  methods: {
    async getData(params = this.$params) {
      params.params.ordering = params.params.sort_by;
      delete params.params.sort_by;
      return await this.$axios(this.url, params).then(
        (response) => (this.items = response.data)
      );
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("user"), key: "user_name_ar" },
        {
          title: this.$t("action"),
          key: "action",
          type: "object",
          val: ["ar"],
        },
        {
          title: this.$t("screen_type"),
          key: "viewset",
          type: "object",
          val: ["ar"],
        },
        { title: this.$t("date"), key: "created_at" },
        {
          title: this.$t("client_info"),
          align: "center",
          key: "client_info",
          children: [
            { title: "ip" },
            {
              title: "device",
              key: "device",
              align: "center",
              children: [
                { title: "os" },
                { title: "is_pc" },
                { title: "device" },
                { title: "browser" },
                { title: "is_mobile" },
                { title: "is_tablet" },
                { title: "is_touch_capable" },
              ],
            },
          ],
        },
      ];
    },
  },
};
</script>
 
