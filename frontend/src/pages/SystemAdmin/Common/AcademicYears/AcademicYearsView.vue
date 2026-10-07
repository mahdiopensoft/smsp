<template>
  <div>
    <add-academic-years v-model="drawer" :data="data" :getData="getData" />
    <custom-data-table v-bind="{
      items,
      getData,
      headers,
      delItem: url,
      editItem,
      create: () => (drawer = true),
    }" :hasFilter="false" :log="false" :restore="false" />
  </div>
</template>

<script>
import AddAcademicYears from './AddAcademicYears.vue';

export default {
  name: 'AcademicYearsView',
  components: {
    AddAcademicYears,
  },
  data() {
    return {
      data: {},
      items: {},
      drawer: false,
      url: "api/academic/academic-years/",
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
        { title: "السنة الهجرية", key: "hijri_year", align: "center", sortable: true },
        { title: "السنة الميلادية", key: "gregorian_year", align: "center", sortable: true },
        { title: "السنة الحالية", key: "is_current", align: "center", width: "120px" },
        { title: "الحالة", key: "is_active", align: "center", width: "100px" },
      ];
    },
  },
};
</script>
