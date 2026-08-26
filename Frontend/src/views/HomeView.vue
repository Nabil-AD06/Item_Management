<script setup lang="ts">
import Sidebar from "../components/layout/Sidebar.vue";
import Header from "@/components/layout/Header.vue";
import request from "@/components/requests/request.vue";
import { get_requests, delete_request_item } from "../services/request.service";
import { ref, onMounted, computed } from "vue";
import { useRouter } from "vue-router";

const activeTab = ref("");
const selectedRequest = ref<Request | null>(null);

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

const requests = ref<Request[]>([]);

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

const router = useRouter();
const goToHistory = () => {
  router.push("/History");
};

const recentRequests = computed(() => {
  return requests.value.slice(0, 5);
});

const overdueRequests = computed(() => {
  const today = new Date();

  return requests.value.filter((request) => {
    if (!request.return_date) {
      return false;
    }

    const returnDate = new Date(request.return_date);

    const isOverdue = returnDate < today;

    const isReturned = request.items.every(
      (item) => item.status === "Returned",
    );

    return isOverdue && !isReturned;
  });
});

const getDaysLate = (returnDate: string | null) => {
  if (!returnDate) {
    return 0;
  }

  const today = new Date();
  const deadline = new Date(returnDate);

  const difference = today.getTime() - deadline.getTime();

  return Math.max(0, Math.floor(difference / (1000 * 60 * 60 * 24)));
};

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

          <button
            class="new-request-btn"
            @click="
              editingRequest = null;
              activeTab = 'request';
            "
          >
            <span>+</span>
            New Request
          </button>
        </div>

        <div class="requests-container">
          <div class="table-header">
            <div>
              <h2>Recent Requests</h2>
              <p>Latest equipment requests</p>
            </div>

            <button class="view-all-btn" @click="goToHistory">View All</button>
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
                <template v-for="request in recentRequests" :key="request.id">
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
          </div>
        </div>
        <div class="overdue-container">
          <div class="table-header">
            <div>
              <h2>Overdue Returns</h2>
              <p>Employees who have not returned their equipment on time</p>
            </div>

            <span class="overdue-count">
              {{ overdueRequests.length }} overdue
            </span>
          </div>

          <div v-if="overdueRequests.length > 0" class="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>REQ ID</th>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Department</th>
                  <th>Return Date</th>
                  <th>Days Late</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="request in overdueRequests" :key="request.id">
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
                    {{ request.department }}
                  </td>

                  <td>
                    {{ request.return_date }}
                  </td>

                  <td>{{ getDaysLate(request.return_date) }} days</td>

                  <td>
                    <span class="status overdue"> Overdue </span>
                  </td>

                  <td>
                    <div class="left-actions">
                      <button
                        class="details-btn"
                        @click="selectedRequest = request"
                      >
                        Details
                      </button>
                      <button class="edit-btn" @click="editRequest(request)">
                        Edit
                      </button>

                      <button
                        @click="deleteItem(item)"
                        class="deleted-btn"
                      >Delete</button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-else class="no-overdue">
            <p>✓ No overdue equipment returns</p>
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
            selectedRequest = null;
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

.request-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
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

.status {
  padding: 6px 12px;
  border-radius: 20px;
  background: #fff7ed;
  color: #c2410c;
  font-weight: 600;
  font-size: 13px;
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

.table-toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
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

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
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
  font-size: 12px;
  font-weight: 600;
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

.actions {
  display: flex;
  align-items: center;
  width: 100%;
}

.left-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  transform: translateX(-25px);
}

table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

th:nth-child(1),
td:nth-child(1) {
  width: 11%;
}

th:nth-child(2),
td:nth-child(2) {
  width: 10%;
}

th:nth-child(3),
td:nth-child(3) {
  width: 12%;
}

th:nth-child(4),
td:nth-child(4) {
  width: 14%;
}

th:nth-child(5),
td:nth-child(5) {
  width: 16%;
}

th:nth-child(6),
td:nth-child(6) {
  width: 10%;
}

th:nth-child(7),
td:nth-child(7) {
  width: 12%;
}

th:nth-child(8),
td:nth-child(8) {
  width: 15%;
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

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 22px;
}

.table-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #1f2937;
}

.table-header p {
  margin: 5px 0 0;
  font-size: 14px;
  color: #64748b;
}

.view-all-btn {
  padding: 10px 18px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: white;
  color: #374151;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.view-all-btn:hover {
  background: #d71920;
  border-color: #d71920;
  color: white;
}

.overdue-container {
  margin-top: 25px;
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.overdue-container table {
  width: 100%;
  table-layout: fixed;
}

.overdue-container .actions {
  justify-content: flex-end;
  padding-right: 110px;
}

.overdue-count {
  padding: 7px 12px;
  border-radius: 20px;
  background: #fee2e2;
  color: #b91c1c;
  font-size: 13px;
  font-weight: 600;
}

.status.overdue {
  background: #fee2e2;
  color: #b91c1c;
}

.no-overdue {
  padding: 30px;
  text-align: center;
  color: #15803d;
  background: #f0fdf4;
  border-radius: 10px;
  font-weight: 600;
}

.delete-btn {
  margin-left: auto;
  margin-right: 0;
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

.deleted-btn{
  margin-left: auto;
  margin-right: 0;
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
.deleted-btn:hover {
  background: #dc2626;
  color: white;
  border-color: #dc2626;
}
</style>
