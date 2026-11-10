<template>
  <v-form ref="form">

    <!-- Top form fields panel -->
    <v-card v-if="withFields" elevation="0" rounded="0" class="hide-item border-b">

      <!-- Header row: title on left, actions on right -->
      <div class="d-flex align-center justify-space-between px-4 py-2 border-b">
        <div class="d-flex align-center gap-2">
          <v-icon color="primary" size="18">mdi-table-plus</v-icon>
          <span class="text-body-2 font-weight-bold" style="color: rgb(var(--v-theme-on-surface))">
            {{ index_item >= 0
              ? ($i18n.locale == 'ar' ? 'تعديل السجل' : 'Edit Record')
              : ($i18n.locale == 'ar' ? 'إضافة سجل جديد' : 'Add New Record') }}
          </span>
        </div>
        <div class="d-flex align-center gap-2">
          <custom-btn
            :type="index_item >= 0 ? 'update' : 'add'"
            @click="index_item >= 0 ? update() : add()"
          />
          <custom-btn
            v-if="index_item >= 0"
            type="cancel"
            @click="(index_item = undefined), (data = {})"
            is-icon
          />
        </div>
      </div>

      <!-- Fields: full-width, stacked layout -->
      <div class="px-4 py-3 fields-panel">
        <v-row>

        <fields :data="data" :fields="filter_fields" />
        <slot name="fields" :item="data" />
        </v-row>
      </div>

    </v-card>

    <!-- Top slot (when no withFields) -->
    <div v-if="!withFields" class="d-flex align-center px-4 py-3 custom-data-table-toolbar bg-surface border-b gap-2">
      <div class="d-flex align-center gap-2">
        <custom-btn
          :type="index_item >= 0 ? 'update' : 'add'"
          @click="index_item >= 0 ? update() : add()"
        />
        <custom-btn
          v-if="index_item >= 0"
          type="cancel"
          @click="(index_item = undefined), (value = {})"
          is-icon
        />
      </div>
    </div>

  </v-form>

  <VDataTableVirtual
    :headers="filter_headers"
    :items="items"
    :no-data-text="$t('not-found')"
    density="compact"
    class="custom-data-table border-sm"
  >
    <template #no-data>
      <NotFound />
    </template>
    <template v-slot:item.actions="{ item, index }">
      <span v-if="actions" class="d-flex align-center gap-1">
        <!-- Edit/Update button -->
        <custom-btn
          type="update"
          is-icon
          variant="tonal"
          class="row-action-btn"
          :click="() => edit(item, index)"
        />
        <!-- Delete/Remove button -->
        <custom-btn
          type="del"
          is-icon
          variant="tonal"
          class="row-action-btn"
          :click="() => remove(index)"
        />
      </span>
    </template>
    <template
      v-for="(slot, name) in $slots"
      :slot="name"
      v-slot:[name]="scope"
      :key="slot"
    >
      <slot :name="name" v-bind="scope"> </slot>
    </template>
  </VDataTableVirtual>
</template>



<script>
import NotFound from "../../other/NotFound.vue";

export default {
  components: {
    NotFound,
  },
  props: {
    headers: {
      type: Array,
      default: [],
    },
    items: {
      type: Array,
      default: [],
    },
    actions: {
      type: Boolean,
      default() {
        return true;
      },
    },
    fields: {
      type: Array,
      default() {
        return [];
      },
    },
    withFields: {
      type: Boolean,
      default() {
        return true;
      },
    },
    modelValue: {
      type: Object,
    },
  },
  data() {
    return {
      data: {},
      index_item: undefined,
    };
  },

  methods: {
    async add() {
      const { valid } = await this.$refs.form.validate();
      if (valid) {
        if (this.withFields) {
          this.items.push({ ...this.data });
          this.data = {};
        } else {
          this.items.push({ ...this.value });
          this.value = {};
        }
      }
    },
    remove(index) {
      this.items.splice(index, 1);
    },
    edit(item, index) {
      if (this.withFields) this.data = { ...item };
      else this.value = { ...item };

      this.index_item = index;
    },
    async update() {
      const { valid } = await this.$refs.form.validate();
      if (valid) {
        if (this.withFields) {
          this.items[this.index_item] = { ...this.data };
          this.index_item = undefined;
          this.data = {};
        } else {
          this.items[this.index_item] = { ...this.value };
          this.index_item = undefined;
          this.value = {};
        }
      }
    },
  },
  computed: {
    value: {
      get() {
        return this.modelValue;
      },
      set(value) {
        this.$emit("update:modelValue", value);
      },
    },

    filter_fields() {
      var list = [];
      this.headers.map((e) => {
        if (e.field) list.push(e.field);
      });
      return list;
    },
    filter_headers() {
      if (this.actions)
        return [
          ...this.headers,
          { title: this.$t("actions"), key: "actions", sortable: false },
        ];
      else return this.headers;
    },
  },
};
</script>
