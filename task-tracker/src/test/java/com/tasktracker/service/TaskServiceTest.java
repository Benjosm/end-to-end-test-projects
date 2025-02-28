package com.tasktracker.service;

import com.tasktracker.model.Task;
import com.tasktracker.model.User;
import com.tasktracker.repository.TaskRepository;
import com.tasktracker.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
public class TaskServiceTest {

    @Mock
    private TaskRepository taskRepository;

    @Mock
    private UserRepository userRepository;

    @InjectMocks
    private TaskService taskService;

    private Task sampleTask;
    private User sampleUser;

    @BeforeEach
    void setUp() {
        sampleUser = new User("testuser", "password", "test@example.com");
        sampleUser.setId(1L);

        sampleTask = new Task("Test Task", "Description for test task", "TODO");
        sampleTask.setId(1L);
        sampleTask.setCreatedAt(LocalDateTime.now());
        sampleTask.setUpdatedAt(LocalDateTime.now());
        sampleTask.setAssignedTo(sampleUser);
    }

    @Test
    void testGetAllTasks() {
        when(taskRepository.findAll()).thenReturn(List.of(sampleTask));
        
        List<Task> tasks = taskService.getAllTasks();
        
        assertEquals(1, tasks.size());
        assertEquals("Test Task", tasks.get(0).getTitle());
        verify(taskRepository).findAll();
    }

    @Test
    void testGetTaskById() {
        when(taskRepository.findById(1L)).thenReturn(Optional.of(sampleTask));
        
        Optional<Task> foundTask = taskService.getTaskById(1L);
        
        assertTrue(foundTask.isPresent());
        assertEquals("Test Task", foundTask.get().getTitle());
        verify(taskRepository).findById(1L);
    }

    @Test
    void testCreateTask() {
        when(taskRepository.save(any(Task.class))).thenReturn(sampleTask);
        
        Task newTask = new Task("New Task", "New Description", "TODO");
        Task createdTask = taskService.createTask(newTask);
        
        assertNotNull(createdTask);
        assertEquals("Test Task", createdTask.getTitle());
        verify(taskRepository).save(any(Task.class));
    }

    @Test
    void testUpdateTask() {
        when(taskRepository.findById(1L)).thenReturn(Optional.of(sampleTask));
        when(taskRepository.save(any(Task.class))).thenReturn(sampleTask);
        
        Task updateDetails = new Task("Updated Task", "Updated Description", "IN_PROGRESS");
        Optional<Task> updatedTask = taskService.updateTask(1L, updateDetails);
        
        assertTrue(updatedTask.isPresent());
        verify(taskRepository).findById(1L);
        verify(taskRepository).save(any(Task.class));
    }

    @Test
    void testDeleteTask() {
        when(taskRepository.existsById(1L)).thenReturn(true);
        doNothing().when(taskRepository).deleteById(1L);
        
        boolean result = taskService.deleteTask(1L);
        
        assertTrue(result);
        verify(taskRepository).existsById(1L);
        verify(taskRepository).deleteById(1L);
    }

    @Test
    void testAssignTaskToUser() {
        when(taskRepository.findById(1L)).thenReturn(Optional.of(sampleTask));
        when(userRepository.findById(1L)).thenReturn(Optional.of(sampleUser));
        when(taskRepository.save(any(Task.class))).thenReturn(sampleTask);
        
        Optional<Task> result = taskService.assignTaskToUser(1L, 1L);
        
        assertTrue(result.isPresent());
        assertEquals(sampleUser, result.get().getAssignedTo());
        verify(taskRepository).findById(1L);
        verify(userRepository).findById(1L);
        verify(taskRepository).save(any(Task.class));
    }
}
