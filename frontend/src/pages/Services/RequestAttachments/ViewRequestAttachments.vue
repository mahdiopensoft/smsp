<template>
  <custom-data-table
    :="{
      headers:request_id?headers.slice(2):headers,
      items,
      getData,
      delItem: url,
      pagination: request_id ? false : true,
      showTop: request_id ? false : true,
    }"
  >
    <!-- actionList, -->
    <template v-slot:item-slot="{ item, key }">
      <span
        class="text-decoration-underline text-primary font-weight-medium cursor-pointer"
        v-if="key == 'request_name'"
        @click="
          moveToNex('request-details', { request_id: item['request_no'] }, {})
        "
      >
        {{ item[key] }}
      </span>
      <span v-if="key=='file_url'">
        <a :href="item[key]" download class="text-decoration-none text-primary font-weight-medium">
          تحميل
        </a>
      </span>
      <span v-if="['file_size'].includes(key)" class="font-mono text-caption text-lowercase">
        {{ item[key] }}
      </span>
      <span v-if="key == 'file_type'" class="text-body-2 font-weight-medium">
        {{ item[key] }}
      </span>
    </template>
  </custom-data-table>
</template>
<script>
export default {
  props: {
    request_id: Number,
    default: null,
  },
  data() {
    return {
      data: {},
      items: [],
      drawer: false,

      url: "d-services/services/attachments/",
      fileTypes: {
        PDF: {
          icon: "mdi-file-pdf-box",
          color: "red-darken-2",
        },
        Word: {
          icon: "mdi-file-work-box",
          color: "blue-darken-2",
        },

        Excel: {
          icon: "mdi-file-excel-box",
          color: "green-darken-2",
        },
        Image: {
          icon: "mdi-file-image",
          color: "deep-purple-darken-2",
        },
        Archive: {
          icon: "mdi-folder-zip-outline",
          color: "amber-darken-2",
        },
      },
    };
  },
  methods: {
    async getData(params = this.$params) {
      if (this.request_id) {
        const filters = {
          filters: [{ field: "fk_instance", value: this.request_id }],
        };
        return await this.$axios
          .post(`${this.url}filter/`, filters)
          .then((response) => {
            this.items = response.data;
            console.log(response.data, "======");
          });
      } else {
        return await this.$axios(this.url, params).then(
          (response) => (this.items = response.data)
        );
      }
    },
    moveToNex(screen, param, query) {
      this.$navigateTo({
        name: screen,
        params: param,
        query: query,
        blank: false,
      });
    },
    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },

    moveToNex(screen, param, query) {
      this.$navigateTo({
        name: screen,
        params: param,
        query: query,
        blank: false,
      });
    },
  },
  computed: {
    headers() {
      return [
        { title: this.$t("request"), key: "request_name" },
        { title: this.$t("request_no"), key: "request_no" },
        { title: this.$t("file_name"), key: "file_name" },
        { title: this.$t("download"), key: "file_url"},
        {
          title: this.$t("file_type"),
          key: "file_type",
        },
        { title: this.$t("file_size"), key: "file_size" },
        { title: this.$t("uploaded_at"), key: "uploaded_at" },
        { title: this.$t("uploaded_by"), key: "fk_uploaded_by_name" },
      ];
    },
  },
};
</script>
