<script setup lang="ts">
import Sidebar from "../components/layout/Sidebar.vue";
import Header from "@/components/layout/Header.vue";
import request from "@/components/requests/request.vue";
import { get_requests, delete_request_item } from "../services/request.service";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";

const activeTab = ref("");
const searchText = ref("");
const filterType = ref("request");
const selectedRequest = ref<Request | null>(null);

const currentPage = ref(1);
const itemsPerPage = 10;
const totalPages = computed(() =>
  Math.ceil(filteredRequests.value.length / itemsPerPage),
);

const paginatedRequests = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;

  return filteredRequests.value.slice(start, start + itemsPerPage);
});

const accessoryOptions = [
  "Headset",
  "Mouse",
  "Keyboard",
  "Laptop",
  "Desktop",
  "Monitor",
  "WebCam",
  "Other",
];

const statusOptions = ["Pending", "Issued", "Returned"];

const editingRequest = ref<Request | null>(null);

interface RequestItem {
  id: number;
  status: string;
  accessory_req: string;
  brand_model: string;
  serial_Number: string;
  quantity: number;
  request: number;
}

interface Request {
  id: number;
  request_id: string;
  issue_date: string | null;
  return_date: string | null;
  employee_id: string;
  employee_name: string;
  employee_email: string;
  department: string;
  reason: string;
  remarks: string;
  date_issued: string | null;
  created_at: string;
  updated_at: string;
  created_by: string;
  items: RequestItem[];
}

const filteredRequests = computed(() => {
  if (!searchValue.value) {
    return requests.value;
  }

  const value = searchValue.value.toLowerCase();

  return requests.value.filter((request) => {
    if (searchType.value === "request") {
      return request.request_id.toLowerCase().includes(value);
    }

    if (searchType.value === "id") {
      return request.employee_id.toLowerCase().includes(value);
    }

    if (searchType.value === "accessory") {
      const accessorySearch =
        searchValue.value === "Other"
          ? customAccessory.value
          : searchValue.value;

      if (!accessorySearch) {
        return true;
      }

      return request.items.some((item) =>
        item.accessory_req
          .toLowerCase()
          .includes(accessorySearch.toLowerCase()),
      );
    }

    if (searchType.value === "status") {
      return request.items.some((item) => item.status.toLowerCase() === value);
    }

    return true;
  });
});

const requests = ref<Request[]>([]);
const searchType = ref("request");
const searchValue = ref("");
const customAccessory = ref("");

const editRequest = (request: Request) => {
  editingRequest.value = request;
  activeTab.value = "request";
};

const loadRequests = async () => {
  const response = await get_requests();
  requests.value = response.data;
};

onMounted(() => {
  loadRequests();
});

const deleteItem = async (item: RequestItem) => {
  const confirmed = confirm(`Voulez-vous vraiment supprimer cet item ?`);

  if (!confirmed) {
    return;
  }

  try {
    await delete_request_item(item.id);

    await loadRequests();

    alert("Item deleted successfully.");
  } catch (error) {
    console.error("Error deleting item:", error);
    alert("Failed to delete item.");
  }
};
</script>

<template>
  <div class="layout">
    <Sidebar />
    <div class="content" :class="{ blur: activeTab !== '' }">
      <Header />

      <main>
        <div class="page-header">
          <div>
            <h1>Equipment Requests</h1>
            <p>Manage and track all equipment requests</p>
          </div>
        </div>

        <div class="requests-container">
          <div class="table-toolbar">
            <!-- Type de recherche -->
            <select v-model="searchType" class="filter-select">
              <option value="request">Request</option>
              <option value="id">ID</option>
              <option value="accessory">Accessory</option>
              <option value="status">Status</option>
            </select>

            <!-- Recherche Request -->
            <input
              v-if="searchType === 'request'"
              v-model="searchValue"
              type="text"
              placeholder="Search request..."
              class="search-input"
            />

            <!-- Recherche ID -->
            <input
              v-if="searchType === 'id'"
              v-model="searchValue"
              type="text"
              placeholder="Search employee ID..."
              class="search-input"
            />

            <!-- Recherche Accessory -->
            <template v-if="searchType === 'accessory'">
              <select v-model="searchValue" class="filter-select">
                <option value="">All Accessories</option>

                <option
                  v-for="accessory in accessoryOptions"
                  :key="accessory"
                  :value="accessory"
                >
                  {{ accessory }}
                </option>
              </select>

              <input
                v-if="searchValue === 'Other'"
                v-model="customAccessory"
                type="text"
                placeholder="Enter accessory..."
                class="search-input"
              />
            </template>

            <!-- Recherche Status -->
            <template v-if="searchType === 'status'">
              <select v-model="searchValue" class="filter-select">
                <option value="">All Statuses</option>

                <option
                  v-for="status in statusOptions"
                  :key="status"
                  :value="status"
                >
                  {{ status }}
                </option>
              </select>
            </template>
          </div>
          <div class="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>REQ ID</th>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Accessory</th>
                  <th>Brand / Model</th>
                  <th>Quantity</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                <template
                  v-for="request in paginatedRequests"
                  :key="request.id"
                >
                  <tr v-for="item in request.items" :key="item.id">
                    <td>
                      <strong>{{ request.request_id }}</strong>
                    </td>

                    <td>
                      {{ request.employee_id }}
                    </td>

                    <td>
                      {{ request.employee_name || "—" }}
                    </td>
                    <td>
                      {{ item.accessory_req }}
                    </td>

                    <td>
                      {{ item.brand_model || "—" }}
                    </td>

                    <td>
                      {{ item.quantity }}
                    </td>

                    <td>
                      <span class="status" :class="item.status.toLowerCase()">
                        {{ item.status }}
                      </span>
                    </td>

                    <td>
                      <div class="actions">
                        <div class="left-actions">
                          <button
                            class="details-btn"
                            @click="selectedRequest = request"
                          >
                            Details
                          </button>

                          <button
                            class="edit-btn"
                            @click="editRequest(request)"
                          >
                            Edit
                          </button>
                        </div>
                        <button @click="deleteItem(item)" class="delete-btn">
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>
            <div class="pagination">
              <button @click="currentPage--" :disabled="currentPage === 1">
                Previous
              </button>

              <span> Page {{ currentPage }} / {{ totalPages }} </span>

              <button
                @click="currentPage++"
                :disabled="currentPage === totalPages"
              >
                Next
              </button>
            </div>
          </div>
        </div>

        <RouterView />
      </main>
    </div>
    <div
      v-if="activeTab === 'request' || activeTab === 'edit'"
      class="modal-overlay"
      @click.self="activeTab = ''"
    >
      <div class="modal">
        <<request
          :editRequest="editingRequest"
          @created="
            activeTab = '';
            selectedRequest = undefined;
            loadRequests();
          "
        />
      </div>
    </div>
    <!-- Details Modal -->
    <div
      v-if="selectedRequest"
      class="modal-overlay"
      @click.self="selectedRequest = null"
    >
      <div class="details-modal">
        <div class="details-header">
          <div>
            <h2>{{ selectedRequest.request_id }}</h2>
            <p>Equipment Request Details</p>
          </div>

          <button class="close-btn" @click="selectedRequest = null">×</button>
        </div>

        <!-- Request Information -->
        <div class="details-section">
          <h3>Request Information</h3>

          <div class="details-grid">
            <div>
              <span>Request ID</span>
              <strong>{{ selectedRequest.request_id }}</strong>
            </div>

            <div>
              <span>Issue Date</span>
              <strong>
                {{ selectedRequest.issue_date || "—" }}
              </strong>
            </div>

            <div>
              <span>Return Date</span>
              <strong>
                {{ selectedRequest.return_date || "—" }}
              </strong>
            </div>

            <div>
              <span>Date Issued</span>
              <strong>
                {{ selectedRequest.date_issued || "—" }}
              </strong>
            </div>

            <div>
              <span>Department</span>
              <strong>{{ selectedRequest.department }}</strong>
            </div>
          </div>
        </div>

        <!-- Employee Information -->
        <div class="details-section">
          <h3>Employee Information</h3>

          <div class="details-grid">
            <div>
              <span>Employee ID</span>
              <strong>{{ selectedRequest.employee_id }}</strong>
            </div>

            <div>
              <span>Name</span>
              <strong>
                {{ selectedRequest.employee_name || "—" }}
              </strong>
            </div>

            <div>
              <span>Email</span>
              <strong>
                {{ selectedRequest.employee_email || "—" }}
              </strong>
            </div>
          </div>
        </div>

        <!-- Equipment -->
        <div class="details-section">
          <h3>Equipment</h3>

          <div
            v-for="item in selectedRequest.items"
            :key="item.id"
            class="equipment-detail"
          >
            <div>
              <span>Accessory</span>
              <strong>{{ item.accessory_req }}</strong>
            </div>

            <div>
              <span>Brand / Model</span>
              <strong>
                {{ item.brand_model || "—" }}
              </strong>
            </div>

            <div>
              <span>Serial Number</span>
              <strong>
                {{ item.serial_Number || "—" }}
              </strong>
            </div>

            <div>
              <span>Quantity</span>
              <strong>{{ item.quantity }}</strong>
            </div>

            <div>
              <span>Status</span>
              <strong>{{ item.status }}</strong>
            </div>
          </div>
        </div>

        <!-- Additional Details -->
        <div class="details-section">
          <h3>Additional Details</h3>

          <div class="details-grid">
            <div>
              <span>Reason</span>
              <strong>
                {{ selectedRequest.reason || "—" }}
              </strong>
            </div>

            <div>
              <span>Remarks</span>
              <strong>
                {{ selectedRequest.remarks || "—" }}
              </strong>
            </div>

            <div>
              <span>Created By</span>
              <strong>
                {{ selectedRequest.created_by }}
              </strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.blur {
  filter: blur(5px);
  pointer-events: none;
  user-select: none;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.35);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  width: 90%;
  max-width: 1590px;
  max-height: 93vh;
  overflow-y: auto;
  background: white;
  border-radius: 19px;
  padding: 15px;
  margin-left: 170px;
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

.request-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.toolbar {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.plus {
  font-size: 22px;
  font-weight: bold;
}

.toolbar button {
  padding: 24px;
  border: none;
  border-radius: 18px;
  background: rgb(233, 223, 223);
  color: #374151;
  font-size: 19px;
  font-weight: 500;
  cursor: pointer;
  transition: 0.3s;
  margin-right: 30px;
}

.toolbar button:hover {
  background: #d71920;
  color: white;
}

main {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
}

.requests-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-top: 30px;
}

.request-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.request-header h2 {
  margin: 0;
  color: #1f2937;
}

.request-header p {
  margin-top: 5px;
  color: #6b7280;
}

.request-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.request-info div {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.request-info span {
  color: #6b7280;
  font-size: 13px;
}

.request-info strong {
  color: #374151;
}

.equipment h3 {
  margin-bottom: 10px;
}

.equipment-item {
  display: grid;
  grid-template-columns: 1fr auto auto;
  gap: 20px;
  padding: 12px;
  margin-top: 8px;
  background: #f9fafb;
  border-radius: 8px;
}

.equipment-item div {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.equipment-item span {
  color: #6b7280;
  font-size: 13px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.page-header h1 {
  margin: 0;
  font-size: 28px;
  color: #1f2937;
}

.page-header p {
  margin-top: 6px;
  color: #64748b;
}

.new-request-btn {
  padding: 14px 22px;
  border: none;
  border-radius: 8px;
  background: #d71920;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

.new-request-btn span {
  font-size: 20px;
  margin-right: 6px;
}

.requests-container {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 20px;
}

/* =========================
   TABLE TOOLBAR / SEARCH & FILTERS
   ========================= */

.table-toolbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 25px;
  padding: 15px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
}

.table-toolbar input {
  width: 380px;
  padding: 12px 15px;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  outline: none;
}

.filter-btn {
  padding: 12px 20px;
  background: white;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  cursor: pointer;
}

/* Input principal de recherche */
.search-input {
  flex: 1;
  min-width: 250px;
  height: 48px;
  width: 300px;
  padding: 0 16px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #ffffff;
  color: #374151;
  font-size: 15px;
  outline: none;
  box-sizing: border-box;
  transition: all 0.2s ease;
}

.search-input::placeholder {
  color: #9ca3af;
}

.search-input:hover {
  border-color: #9ca3af;
}

.search-input:focus {
  border-color: #d71920;
  box-shadow: 0 0 0 3px rgba(215, 25, 32, 0.1);
}

/* Select "Filter by" */
.filter-select {
  height: 48px;
  min-width: 170px;
  padding: 0 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background-color: #ffffff;
  color: #374151;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  outline: none;
  appearance: auto;
  transition: all 0.2s ease;
}

.filter-select:hover {
  border-color: #9ca3af;
}

.filter-select:focus {
  border-color: #d71920;
  box-shadow: 0 0 0 3px rgba(215, 25, 32, 0.1);
}

/* Select Accessory */
.accessory-select {
  height: 48px;
  min-width: 180px;
  padding: 0 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  font-size: 15px;
  color: #374151;
  cursor: pointer;
  outline: none;
}

.accessory-select:focus {
  border-color: #d71920;
}

/* Select Status */
.status-select {
  height: 48px;
  min-width: 160px;
  padding: 0 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  font-size: 15px;
  color: #374151;
  cursor: pointer;
  outline: none;
}

.status-select:focus {
  border-color: #d71920;
}

/* Input affiché lorsque Accessory = Other */
.other-accessory-input {
  height: 48px;
  min-width: 180px;
  padding: 0 14px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 15px;
  outline: none;
}

.other-accessory-input:focus {
  border-color: #d71920;
  box-shadow: 0 0 0 3px rgba(215, 25, 32, 0.1);
}

/* Bouton reset */
.reset-filter-btn {
  height: 48px;
  padding: 0 18px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.reset-filter-btn:hover {
  background: #f3f4f6;
}

.table-wrapper {
  overflow-x: auto;
}

/* =========================
   RESPONSIVE
   ========================= */

@media (max-width: 900px) {
  .table-toolbar {
    flex-wrap: wrap;
  }

  .search-input {
    width: 100%;
    flex-basis: 100%;
  }

  .filter-select,
  .accessory-select,
  .status-select,
  .other-accessory-input {
    flex: 1;
  }
}

@media (max-width: 768px) {
  .table-toolbar {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-select,
  .search-input {
    width: 100%;
  }
}

/* =========================
   TABLE
   ========================= */

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

thead {
  background: #f8fafc;
}

th {
  padding: 15px 12px;
  text-align: left;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  border-bottom: 1px solid #e5e7eb;
}

td {
  padding: 16px 12px;
  border-bottom: 1px solid #eef0f2;
  font-size: 14px;
  color: #374151;
}

tbody tr:hover {
  background: #fafafa;
}

.status {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 6px;
  background: #fff7ed;
  color: #c2410c;
  font-weight: 600;
  font-size: 12px;
}

.status.issued {
  background: #fff7ed;
  color: #ea580c;
}

.status.pending {
  background: #fef3c7;
  color: #b45309;
}

.status.returned {
  background: #dcfce7;
  color: #15803d;
}

/* =========================
   ACTIONS (table rows / modal)
   ========================= */

.actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  width: 100%;
  padding-right: 50px;
}

.details-btn {
  padding: 7px 8px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 100%;
  font-weight: 600;
  background: white;
  border: 1px solid #d1d5db;
  color: #374151;
}

.edit-btn {
  padding: 7px 11px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 600;
  background: #d71920;
  border: 1px solid #d71920;
  color: white;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  transform: translateX(-25px);
}

.delete-btn {
  margin-left: auto;
  margin-right: -40px;
  padding: 7px 11px;
  border-radius: 6px;
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.delete-btn:hover {
  background: #dc2626;
  color: white;
  border-color: #dc2626;
}

/* =========================
   DETAILS MODAL
   ========================= */

.details-modal {
  width: 90%;
  max-width: 900px;
  max-height: 90vh;
  overflow-y: auto;
  background: white;
  border-radius: 14px;
  padding: 30px;
}

.details-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 20px;
  margin-bottom: 25px;
}

.details-header h2 {
  margin: 0;
  font-size: 24px;
  color: #1f2937;
}

.details-header p {
  margin-top: 5px;
  color: #6b7280;
}

.close-btn {
  border: none;
  background: #f3f4f6;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  font-size: 22px;
  cursor: pointer;
}

.details-section {
  margin-bottom: 25px;
}

.details-section h3 {
  margin-bottom: 15px;
  color: #374151;
  font-size: 17px;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.details-grid div,
.equipment-detail div {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.details-grid span,
.equipment-detail span {
  font-size: 12px;
  color: #6b7280;
}

.details-grid strong,
.equipment-detail strong {
  color: #1f2937;
}

.equipment-detail {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
  padding: 18px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 10px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding: 20px;
}

.pagination button {
  padding: 10px 20px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  cursor: pointer;
}

.pagination button:hover:not(:disabled) {
  background: #d71920;
  color: white;
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination span {
  font-weight: 600;
  color: rgb(107, 107, 107);
}
</style>
