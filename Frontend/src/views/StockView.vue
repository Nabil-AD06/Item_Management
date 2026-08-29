<script setup lang="ts">
import { ref, onMounted } from "vue";
import Sidebar from "@/components/layout/Sidebar.vue";
import Header from "@/components/layout/Header.vue";
import {
  get_categories,
  create_category,
  type Category,
} from "@/services/category.service";
import {
  get_equipments,
  create_equipment,
  update_equipment,
  delete_equipment,
  type Equipment,
} from "@/services/equipment.service";

const equipments = ref<Equipment[]>([]);
const showAddModal = ref(false);
const newCategory = ref("");
const selectedCategory = ref<Category | null>(null);
const showItemsModal = ref(false);
const showEquipmentModal = ref(false);
const selectedEquipment = ref<Equipment | null>(null);
const showEditEquipmentModal = ref(false);

const equipmentForm = ref({
  brand_model: "",
  serial_number: "",
  quantity: 1,
  notes: "",
});

const loadEquipments = async () => {
  try {
    const response = await get_equipments();
    equipments.value = response.data;
  } catch (error) {
    console.error("Error loading equipments:", error);
  }
};

const categories = ref<Category[]>([]);

const getCategoryQuantity = (category: Category) => {
  return equipments.value
    .filter(
      (equipment) =>
        equipment.category === category.name &&
        equipment.status === "Available",
    )
    .reduce((total, equipment) => total + equipment.quantity, 0);
};

const addCategory = async () => {
  if (!newCategory.value.trim()) {
    return;
  }

  try {
    await create_category(newCategory.value.trim());

    await loadCategories();

    newCategory.value = "";
    showAddModal.value = false;
  } catch (error) {
    console.error("Error creating category:", error);
  }
};

const loadCategories = async () => {
  try {
    const response = await get_categories();
    categories.value = response.data;
  } catch (error) {
    console.error("Error loading categories:", error);
  }
};

const viewItems = (category: Category) => {
  selectedCategory.value = category;
  showItemsModal.value = true;
};

const openAddEquipment = () => {
  editingEquipment.value = null;

  equipmentForm.value = {
    brand_model: "",
    serial_number: "",
    quantity: 1,
    notes: "",
  };

  showEquipmentModal.value = true;
};

const addEquipment = async () => {
  if (!selectedCategory.value) {
    return;
  }

  try {
    const data = {
      category: selectedCategory.value.name,
      brand_model: equipmentForm.value.brand_model,
      serial_number: equipmentForm.value.serial_number,
      quantity: equipmentForm.value.quantity,
      notes: equipmentForm.value.notes,
    };

    if (editingEquipment.value) {
      // EDIT
      await update_equipment(editingEquipment.value.id, data);
    } else {
      // CREATE
      await create_equipment(data);
    }

    await loadEquipments();

    equipmentForm.value = {
      brand_model: "",
      serial_number: "",
      quantity: 1,
      notes: "",
    };

    editingEquipment.value = null;
    showEquipmentModal.value = false;
  } catch (error) {
    console.error("Error saving equipment:", error);
  }
};

const editingEquipment = ref<Equipment | null>(null);

const openEditEquipment = (equipment: Equipment) => {
  editingEquipment.value = equipment;

  equipmentForm.value = {
    brand_model: equipment.brand_model,
    serial_number: equipment.serial_number,
    quantity: equipment.quantity,
    notes: equipment.notes,
  };

  showEquipmentModal.value = true;
};

const updateEquipment = async () => {
  if (!selectedEquipment.value) {
    return;
  }

  try {
    await update_equipment(selectedEquipment.value.id, {
      category: selectedEquipment.value.category,

      brand_model: equipmentForm.value.brand_model,

      serial_number: equipmentForm.value.serial_number,

      quantity: equipmentForm.value.quantity,

      notes: equipmentForm.value.notes,
    });

    await loadEquipments();

    selectedEquipment.value = null;

    equipmentForm.value = {
      brand_model: "",
      serial_number: "",
      quantity: 1,
      notes: "",
    };

    showEditEquipmentModal.value = false;
  } catch (error) {
    console.error("Error updating equipment:", error);
  }
};

const saveEquipment = async () => {
  if (!selectedCategory.value) {
    return;
  }

  try {
    const data = {
      category: selectedCategory.value.name,
      brand_model: equipmentForm.value.brand_model,
      serial_number: equipmentForm.value.serial_number,
      quantity: equipmentForm.value.quantity,
      notes: equipmentForm.value.notes,
    };

    if (editingEquipment.value) {
      // EDIT
      await update_equipment(editingEquipment.value.id, data);
    } else {
      // CREATE
      await create_equipment(data);
    }

    await loadEquipments();

    equipmentForm.value = {
      brand_model: "",
      serial_number: "",
      quantity: 1,
      notes: "",
    };

    editingEquipment.value = null;
    showEquipmentModal.value = false;
  } catch (error) {
    console.error("Error saving equipment:", error);
  }
};

const resetEquipmentForm = () => {
  equipmentForm.value = {
    brand_model: "",
    serial_number: "",
    quantity: 1,
    notes: "",
  };

  editingEquipment.value = null;
  showEquipmentModal.value = false;
};

const removeEquipment = async (equipment: Equipment) => {
  const confirmed = confirm(
    `Are you sure you want to delete ${equipment.brand_model}?`,
  );

  if (!confirmed) {
    return;
  }

  try {
    await delete_equipment(equipment.id);

    await loadEquipments();
  } catch (error) {
    console.error("Error deleting equipment:", error);
  }
};

onMounted(() => {
  loadEquipments();
  loadCategories();
});
</script>

<template>
  <div class="layout">
    <Sidebar />
    <div class="content">
      <Header />

      <main>
        <div class="page-header">
          <div>
            <h1>Equipment Stock</h1>
            <p>Manage and track your equipment inventory</p>
          </div>
        </div>

        <div class="stock-grid">
          <!-- Categories -->
          <div
            v-for="category in categories"
            :key="category.id"
            class="stock-card"
          >
            <div class="stock-icon">📦</div>

            <div class="stock-info">
              <h2>{{ category.name }}</h2>

              <p>
                {{ getCategoryQuantity(category) }}
                available
              </p>
            </div>

            <button class="view-btn" @click="viewItems(category)">
              View Items
            </button>
          </div>

          <!-- Add Item -->
          <div class="stock-card add-card">
            <div class="add-icon">+</div>

            <h2>Add Category</h2>

            <p>Create a new equipment category</p>

            <button class="add-btn" @click="showAddModal = true">
              Add Category
            </button>
          </div>
        </div>
      </main>
      <div
        v-if="showAddModal"
        class="modal-overlay"
        @click.self="showAddModal = false"
      >
        <div class="modal">
          <div class="modal-header">
            <div>
              <h2>Add Category</h2>
              <p>Create a new equipment category</p>
            </div>

            <button class="close-btn" @click="showAddModal = false">×</button>
          </div>

          <form @submit.prevent="addCategory">
            <div class="form-group">
              <label>Category name</label>

              <input
                v-model="newCategory"
                type="text"
                placeholder="e.g. Mouse"
                required
              />
            </div>

            <div class="modal-actions">
              <button
                type="button"
                class="cancel-btn"
                @click="showAddModal = false"
              >
                Cancel
              </button>

              <button type="submit" class="save-btn">
                {{ editingEquipment ? "Save Changes" : "Add Equipment" }}
              </button>
            </div>
          </form>
        </div>
      </div>
      <div
        v-if="showItemsModal"
        class="modal-overlay"
        @click.self="showItemsModal = false"
      >
        <div class="items-modal">
          <div class="modal-header">
            <div>
              <h2>{{ selectedCategory?.name }}</h2>
              <p>Equipment available in this category</p>
            </div>

            <button class="close-btn" @click="showItemsModal = false">×</button>
          </div>
          <button class="add-equipment-btn" @click="openAddEquipment">
            + Add Equipment
          </button>

          <div class="items-list">
            <div
              v-for="equipment in equipments.filter(
                (equipment) => equipment.category === selectedCategory?.name,
              )"
              :key="equipment.id"
              class="equipment-row"
            >
              <div>
                <strong>{{ equipment.brand_model || "—" }}</strong>
              </div>

              <div>Serial: {{ equipment.serial_number || "—" }}</div>

              <div>Quantity: {{ equipment.quantity }}</div>

              <div>
                Status:
                <span class="status" :class="equipment.status.toLowerCase()">
                  {{ equipment.status }}
                </span>
              </div>
              <div class="equipment-actions">
                <button class="edit-btn" @click="openEditEquipment(equipment)">
                  Edit
                </button>

                <button class="delete-btn" @click="removeEquipment(equipment)">
                  Delete
                </button>
              </div>
            </div>

            <div
              v-if="
                equipments.filter(
                  (equipment) => equipment.category === selectedCategory?.name,
                ).length === 0
              "
              class="empty-items"
            >
              No equipment in this category.
            </div>
          </div>
        </div>
      </div>
      <div
        v-if="showEquipmentModal"
        class="modal-overlay"
        @click.self="showEquipmentModal = false"
      >
        <div class="modal">
          <div class="modal-header">
            <div>
              <h2>
                {{ editingEquipment ? "Edit Equipment" : "Add Equipment" }}
              </h2>
              <p>
                {{
                  editingEquipment
                    ? "Update equipment information"
                    : `Add a new ${selectedCategory?.name} to the stock`
                }}
              </p>
            </div>

            <button class="close-btn" @click="showEquipmentModal = false">
              ×
            </button>
          </div>

          <form @submit.prevent="saveEquipment">
            <div class="form-group">
              <label>Category</label>

              <input type="text" :value="selectedCategory?.name" disabled />
            </div>

            <div class="form-group">
              <label>Brand / Model</label>

              <input
                v-model="equipmentForm.brand_model"
                type="text"
                placeholder="e.g. Dell Precision 5360"
                required
              />
            </div>

            <div class="form-group">
              <label>Serial Number</label>

              <input
                v-model="equipmentForm.serial_number"
                type="text"
                placeholder="Enter serial number"
              />
            </div>

            <div class="form-group">
              <label>Quantity</label>

              <input
                v-model.number="equipmentForm.quantity"
                type="number"
                min="1"
                required
              />
            </div>

            <div class="form-group">
              <label>Notes</label>

              <textarea
                v-model="equipmentForm.notes"
                placeholder="Additional information..."
              ></textarea>
            </div>

            <div class="modal-actions">
              <button
                type="button"
                class="cancel-btn"
                @click="showEquipmentModal = false"
              >
                Cancel
              </button>

              <button type="submit" class="save-btn">
                {{ editingEquipment ? "Save Changes" : "Add Equipment" }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  background: #f8fafc;
}

.blocs {
  color: black;
}

main {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.layout {
  display: flex;
  height: 100vh;
  background: #f8fafc;
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

main {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  margin: 0;
  font-size: 30px;
  color: #1f2937;
}

.page-header p {
  margin-top: 8px;
  color: #6b7280;
}

.stock-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 25px;
}

.stock-card {
  position: relative;
  min-height: 190px;
  padding: 25px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);

  display: flex;
  flex-direction: column;

  transition: 0.2s;
}

.stock-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.stock-icon {
  font-size: 35px;
  margin-bottom: 15px;
}

.stock-info h2 {
  margin: 0;
  color: #1f2937;
  font-size: 22px;
}

.stock-info p {
  margin-top: 8px;
  color: #6b7280;
}

.view-btn {
  margin-top: auto;
  width: fit-content;

  padding: 9px 15px;

  border: none;
  border-radius: 7px;

  background: #f3f4f6;
  color: #374151;

  cursor: pointer;
}

.view-btn:hover {
  background: #d71920;
  color: white;
}

.add-card {
  justify-content: center;
  align-items: center;
  text-align: center;

  border: 2px dashed #d71920;
}

.add-icon {
  font-size: 45px;
  color: #d71920;
  font-weight: bold;
}

.add-card h2 {
  margin: 10px 0 5px;
}

.add-card p {
  color: #6b7280;
}

.add-btn {
  margin-top: 15px;

  padding: 10px 18px;

  border: none;
  border-radius: 8px;

  background: #d71920;
  color: white;

  cursor: pointer;
}

.modal-overlay {
  position: fixed;
  inset: 0;

  background: rgba(0, 0, 0, 0.4);

  display: flex;
  justify-content: center;
  align-items: center;

  z-index: 1000;
}

.modal {
  width: 550px;
  max-width: 90%;

  max-height: 90vh;
  overflow-y: auto;

  background: white;

  border-radius: 18px;

  padding: 25px;

  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;

  margin-bottom: 25px;
}

.modal-header h2 {
  margin: 0;

  font-size: 24px;
  color: #1f2937;
}

.modal-header p {
  margin-top: 6px;

  color: #6b7280;
}

.close-btn {
  border: none;
  background: transparent;

  font-size: 28px;

  cursor: pointer;

  color: #6b7280;
}

.close-btn:hover {
  color: #d71920;
}

.form-group {
  display: flex;
  flex-direction: column;

  margin-bottom: 18px;
}

.form-group label {
  margin-bottom: 7px;

  font-size: 14px;
  font-weight: 600;

  color: #374151;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;

  box-sizing: border-box;

  padding: 11px 12px;

  border: 1px solid #d1d5db;

  border-radius: 8px;

  font-size: 14px;

  outline: none;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #d71920;
}

.form-group textarea {
  min-height: 90px;

  resize: vertical;
}

.modal-actions {
  display: flex;

  justify-content: flex-end;

  gap: 10px;

  margin-top: 25px;
}

.cancel-btn,
.save-btn {
  padding: 11px 18px;

  border-radius: 8px;

  cursor: pointer;

  font-size: 14px;
  font-weight: 500;
}

.cancel-btn {
  border: 1px solid #d1d5db;

  background: white;

  color: #374151;
}

.save-btn {
  border: none;

  background: #d71920;

  color: white;
}

.save-btn:hover {
  background: #b9151b;
}

.items-modal {
  width: 900px;
  max-width: 90%;
  max-height: 85vh;
  overflow-y: auto;
  background: white;
  border-radius: 18px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.items-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.equipment-row {
  display: grid;
  grid-template-columns: 1.5fr 1.5fr 1fr 1fr;
  align-items: center;
  gap: 15px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #f9fafb;
}

.equipment-row strong {
  color: #1f2937;
}

.equipment-row div {
  color: #4b5563;
  font-size: 14px;
}
.add-equipment-btn {
  margin-bottom: 20px;
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  background: #d71920;
  color: white;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.add-equipment-btn:hover {
  background: #b9151b;
}
.status {
  padding: 5px 9px;
  border-radius: 6px;
  font-size: 12px;
  font-weight: 600;
}

.status.available {
  background: #dcfce7;
  color: #166534;
}

.status.pending {
  background: #fef3c7;
  color: #92400e;
}

.status.issued {
  background: #fee2e2;
  color: #991b1b;
}

.empty-items {
  text-align: center;
  padding: 40px;
  color: #6b7280;
}

.equipment-actions {
  display: flex;
  gap: 8px;
  margin-left: auto;
}

.edit-btn,
.delete-btn {
  border: none;
  padding: 8px 12px;
  border-radius: 7px;
  cursor: pointer;
  font-size: 13px;
}

.edit-btn {
  background: #f3f4f6;
  color: #374151;
}

.edit-btn:hover {
  background: #d71920;
  color: white;
}

.delete-btn {
  background: #fee2e2;
  color: #dc2626;
}

.delete-btn:hover {
  background: #dc2626;
  color: white;
}
</style>
