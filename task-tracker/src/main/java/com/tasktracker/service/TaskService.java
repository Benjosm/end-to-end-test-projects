package com.tasktracker.service;

import com.tasktracker.model.Task;
import com.tasktracker.model.User;
import com.tasktracker.repository.TaskRepository;
import com.tasktracker.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import javax.transaction.Transactional;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class TaskService {
    
    private final TaskRepository taskRepository;
    private final UserRepository userRepository;
    
    @Autowired
    public TaskService(TaskRepository taskRepository, UserRepository userRepository) {
        this.taskRepository = taskRepository;
        this.userRepository = userRepository;
    }
    
    public List<Task> getAllTasks() {
        return taskRepository.findAll();
    }
    
    public Optional<Task> getTaskById(Long id) {
        return taskRepository.findById(id);
    }
    
    public List<Task> getTasksByStatus(String status) {
        return taskRepository.findByStatus(status);
    }
    
    public List<Task> getTasksByUser(Long userId) {
        Optional<User> user = userRepository.findById(userId);
        return user.map(taskRepository::findByAssignedTo).orElse(List.of());
    }
    
    @Transactional
    public Task createTask(Task task) {
        task.setCreatedAt(LocalDateTime.now());
        task.setUpdatedAt(LocalDateTime.now());
        return taskRepository.save(task);
    }
    
    @Transactional
    public Optional<Task> updateTask(Long id, Task taskDetails) {
        return taskRepository.findById(id)
                .map(existingTask -> {
                    existingTask.setTitle(taskDetails.getTitle());
                    existingTask.setDescription(taskDetails.getDescription());
                    existingTask.setStatus(taskDetails.getStatus());
                    existingTask.setDueDate(taskDetails.getDueDate());
                    existingTask.setUpdatedAt(LocalDateTime.now());
                    
                    existingTask.setAssignedTo(taskDetails.getAssignedTo());
                    
                    return taskRepository.save(existingTask);
                });
    }
    
    @Transactional
    public boolean deleteTask(Long id) {
        if (taskRepository.existsById(id)) {
            taskRepository.deleteById(id);
            return true;
        }
        return false;
    }
    
    @Transactional
    public Optional<Task> assignTaskToUser(Long taskId, Long userId) {
        Optional<Task> taskOpt = taskRepository.findById(taskId);
        Optional<User> userOpt = userRepository.findById(userId);
        
        if (taskOpt.isPresent() && userOpt.isPresent()) {
            Task task = taskOpt.get();
            task.setAssignedTo(userOpt.get());
            task.setUpdatedAt(LocalDateTime.now());
            return Optional.of(taskRepository.save(task));
        }
        
        return Optional.empty();
    }
    
    public List<Task> searchTasks(String keyword) {
        return taskRepository.searchTasks(keyword);
    }
    
    public List<Task> getOverdueTasks() {
        return taskRepository.findByDueDateBefore(LocalDateTime.now().plusDays(1));
    }
}
