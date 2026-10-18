<template>
  <!-- added by samer -->
  <v-btn
    icon="mdi-close"
    is-icon
    @click="$router.push({ name: 'groups-management' })"
    style="position: absolute; z-index: 1000; left: 5px;top: 3px;"
    class="bg-red"
    size="25"
  />
  <VForm ref="form">
    <fieldset class="mb-5 border rounded pa-2" v-if="group_id == 0">
      <legend class="mx-2 px-2">
        <span class="text-medium-emphasis">الصلاحيات حسب الشاشة</span>
      </legend>
      <v-row>
        <custom-text-field
          label="اسم المجموعة"
          v-model="group.name"
          cols="4"
          :rules="[$required]"
        />
      </v-row>
    </fieldset>
  </VForm>
  <VRow class="pa-5">
    <v-checkbox
      v-model="selectAll"
      @change="taggleSelectAll"
      :label="selectAll ? 'الغاء تحديد الكل' : 'تحديد الكل'"
    />

    <VSpacer />
    <custom-btn
      v-if="group_id == 0"
      :click="saveGroupPermissions"
      type="save"
    />
    <custom-btn
      v-if="group_id && group_id != 0"
      :click="updateGroupPermissions"
      type="update"
    />
  </VRow>
  <div class="d-flex justify-center mb-3">
    <div></div>
  </div>
  <v-skeleton-loader v-if="loading" :type="`table-row-divider@10`" />

  <v-table v-else>
    <thead>
      <tr>
        <th>اسم الشاشة</th>
        <th
          v-for="(perm, index) in permissionTypes"
          :key="index"

        >
          <v-checkbox

            :label="perm.label"
            @click="toggleColumn(index)"
            :model-value="isColumnSelected(index)"
            color="primary"
            hide-details
            density="compact"
            :indeterminate="
              items.some((item) => item.permissions[index].status == false) &&
              !items.every((item) => item.permissions[index].status == true) &&
              !items.every((item) => item.permissions[index].status == false)
            "
          ></v-checkbox>
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, rowIndex) in items" :key="item.id">
        <td>
          <v-lazy>
            <v-checkbox-btn
            style="width: 200px !important"
              :label="item.name_ar"
              @click="toggleRow(rowIndex)"
              :model-value="isRowSelected(rowIndex)"
              color="primary"
              hide-details
              density="compact"
              :indeterminate="
                items[rowIndex].permissions.some((e) => e.status == false) &&
                !items[rowIndex].permissions.every((e) => e.status == true) &&
                !items[rowIndex].permissions.every((e) => e.status == false)
              "
            ></v-checkbox-btn>
          </v-lazy>
        </td>

        <td v-for="(pre, colIndex) in item.permissions" :key="pre.id">
          <v-lazy style="width: 100px !important">
            <v-icon
              :icon="
                pre.status
                  ? 'mdi-checkbox-marked-circle'
                  : 'mdi-checkbox-blank-circle-outline'
              "
              @click="pre.status = !pre.status"
              :class="[{ 'text-primary': pre.status }, 'ms-1']"
            />
          </v-lazy>
          <!-- <v-icon
              icon="mdi-checkbox-blank-outline"
              v-else
              @click="pre.status = true"
              class="ms-1"
            /> -->
          <!-- <v-lazy>
            <v-checkbox
              v-model="pre.status"
              color="primary"
              hide-details
              density="compact"
            ></v-checkbox>
          </v-lazy> -->
        </td>
      </tr>
    </tbody>
  </v-table>

</template>

<script>
export default {
  data() {
    return {
      loading: true,
      group_id: this.$route.params.id,
      url: "user-manager/screen-with-permissions",
      items: [],
      filter: {},
      group: {
        name: null,
        fk_screen_permission: [],
      },
      permissionTypes: [
        { label: "عرض" },
        { label: "اضافة" },
        { label: "تعديل" },
        { label: "حذف" },
        { label: "اختيار" },
        { label: "تصدير" },
        { label: "استيراد" },
        { label: "استعادة" },
        { label: "عرض المحذوفات" },
      ],
      selectAll: false,
    };
  },
  methods: {

    async getData() {
      try {
        this.loading = true;
        return await this.$axios(this.url).then((response) => {
          var data = response.data;
          data.forEach((screen) => {
            screen.permissions.forEach((per) => {
              if (this.group.fk_screen_permission.includes(per.id))
                per.status = true;
              else per.status = false;
            });
          });
          this.items = data;
        });
      } finally {
        this.loading = false;
      }
    },
    async saveGroupPermissions() {
      const { valid } = await this.$refs.form.validate();

      if (!valid) return;

      var data = [];
      this.items.forEach((screen) => {
        screen.permissions.forEach((per) => {
          if (per.status === true) data.push(per.id);
        });
      });

      this.$axios
        .post("user-manager/groups/", {
          name: this.group.name,
          fk_screen_permission: data,
        })
        .then(() => {
          this.$snack("add");
          this.$router.push({ name: "groups-management" });
        });
    },
    async getGroupPermissions() {
      await this.$axios
        .get(`user-manager/groups/${this.group_id}/`)
        .then((response) => {
          this.getData();
          this.group = response.data;
        });
    },
    async updateGroupPermissions() {
      var data = [];
      this.items.forEach((screen) => {
        screen.permissions.forEach((per) => {
          if (per.status === true) data.push(per.id);
        });
      });

      await this.$axios
        .put(`user-manager/groups/${this.group_id}/`, {
          id: this.group_id,
          fk_screen_permission: data,
        })
        .then((response) => {
          this.$snack("update");
          this.$router.push({ name: "groups-management" });
        });
    },
    taggleSelectAll() {
      this.items.map((e) => {
        e.permissions.map((select) => (select.status = this.selectAll));
      });
    },
    toggleRow(rowIndex) {
      const select = this.isRowSelected(rowIndex);
      this.items[rowIndex].permissions.forEach((e) => (e.status = !select));
    },
    isRowSelected(rowIndex) {
      return this.items[rowIndex].permissions.every((e) => e.status);
    },

    // تحديد الكل من العمود
    toggleColumn(colIndex) {
      const select = this.isColumnSelected(colIndex);
      this.items.forEach((e) => (e.permissions[colIndex].status = !select));
    },

    isColumnSelected(colIndex) {
      const allselect = this.items.every(
        (item) => item.permissions[colIndex].status
      );
      return allselect;
    },
  },
  async created() {
    if (this.group_id && this.group_id != 0) {
      await this.getGroupPermissions();
    } else this.getData();
  },
};
</script>
