package com.tasktracker.repository;

import com.tasktracker.model.Task;
import com.tasktracker.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface TaskRepository extends JpaRepository<Task, Long> {
    
    List<Task> findByStatus(String status);
    
    List<Task> findByAssignedTo(User user);
    
    @Query(value = "SELECT * FROM tasks WHERE title LIKE '%' || :keyword || '%' OR description LIKE '%' || :keyword || '%'", 
           nativeQuery = true)
    List<Task> searchTasks(@Param("keyword") String keyword);
    
    List<Task> findByDueDateBefore(LocalDateTime date);
    
    List<Task> findByStatusAndAssignedTo(String status, User user);
}
