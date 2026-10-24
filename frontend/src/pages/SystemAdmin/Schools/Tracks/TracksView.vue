<template>
  <div>
    <add-tracks v-model="drawer" :data="data" :getData="getData" />

    <!-- Data Table -->
    <custom-data-table
      v-bind="{
        items,
        getData,
        headers,
        delItem: url,
        editItem,
        create: () => (drawer = true),
      }"
      :hasFilter="false"
      :log="false"
      :restore="false"
    >
      <template v-slot:item-slot="{ item, key }">
        <!-- Track Name -->
        <template v-if="key === 'name_ar'">
          <span>{{ item.name_ar || '-' }}</span>
        </template>

        <!-- Code -->
        <template v-else-if="key === 'code'">
          <span>{{ item.code || '-' }}</span>
        </template>

        <!-- Is Active Status -->
        <template v-else-if="key === 'is_active'">
          <v-chip
            size="small"
            :color="item.is_active ? 'success' : 'error'"
            variant="tonal"
            class="font-weight-bold text-white"
          >
            <v-icon start size="14">{{ item.is_active ? 'mdi-check-circle' : 'mdi-close-circle' }}</v-icon>
            {{ item.is_active ? 'مفعل' : 'معطل' }}
          </v-chip>
        </template>
      </template>
    </custom-data-table>
  </div>
</template>

<script>
import AddTracks from './AddTracks.vue';

export default {
  name: 'TracksView',
  components: {
    AddTracks,
  },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "api/academic/tracks/",
    };
  },
  methods: {
    async getData(params = this.$params) {
      return await this.$axios
        .get(this.url, { params: params?.params || params })
        .then((response) => (this.items = response.data));
    },

    editItem(data) {
      this.data = { ...data };
      this.drawer = true;
    },
  },
  computed: {
    headers() {
      return [
        { title: "الاسم (عربي)", key: "name_ar" },
        { title: "الاسم (إنجليزي)", key: "name_en" },
        { title: "الكود", key: "code" },
        { title: "الحالة", key: "is_active" },
        { title: "الملاحظة", key: "note" },
      ];
    },
  },
};
</script>
